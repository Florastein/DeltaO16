import os
import subprocess
import usb.core
import usb.util
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import http.server
import socket
import threading
import ctypes
import sys

KEY = hashlib.sha256(b"EOT").digest()  # Create a 256-bit key from the password

def remove_write_protection():
    try:
        # Run Diskpart commands to remove write protection
        subprocess.run("diskpart", input="list disk\n", text=True, check=True)
        disk_number = input("Enter the USB disk number: ")
        commands = f"select disk {disk_number}\nattributes disk clear readonly\n"
        result = subprocess.run("diskpart", input=commands, text=True, check=True)
        print("Write protection removed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove write protection: {e}")
        return False

def list_files(directory):
    """List all files in a given directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

def delete_file(filepath):
    """Delete a specific file."""
    try:
        os.remove(filepath)
        print(f"Deleted: {filepath}")
    except Exception as e:
        print(f"Error deleting {filepath}: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def encrypt_file(filepath):
    """Encrypt a file using AES-256."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        cipher = AES.new(KEY, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        
        with open(filepath, 'wb') as f:
            f.write(cipher.iv + ciphertext)
        
        print(f"Encrypted: {filepath}")
    except Exception as e:
        print(f"Error encrypting {filepath}: {e}")

def decrypt_file(filepath):
    """Decrypt a file using AES-256."""
    try:
        with open(filepath, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()
        
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        with open(filepath, 'wb') as f:
            f.write(data)
        
        print(f"Decrypted: {filepath}")
    except Exception as e:
        print(f"Error decrypting {filepath}: {e}")

def read_usb():
    # Find the USB device
    dev = usb.core.find(find_all=True)

    if dev is None:
        raise ValueError("No USB device found")

    for device in dev:
        print(f"Device: {device}")
        print(f"  Manufacturer: {usb.util.get_string(device, device.iManufacturer)}")
        print(f"  Product: {usb.util.get_string(device, device.iProduct)}")
        print(f"  Serial Number: {usb.util.get_string(device, device.iSerialNumber)}")

    # Mount the USB device and get the mount point
    mount_point = '/mnt/usb'
    if not os.path.ismount(mount_point):
        os.makedirs(mount_point, exist_ok=True)
        os.system(f"mount /dev/sda1 {mount_point}")

    return mount_point

def encrypt_all_files(directory):
    """Encrypt all files in the given directory recursively."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            encrypt_file(filepath)

def decrypt_all_files(directory):
    """Decrypt all files in the given directory recursively."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            decrypt_file(filepath)

def serve(directory, host='localhost', port=8000):
    """Serve files in the given directory using HTTP."""
    os.chdir(directory)
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    print(f"Server started at http://{host}:{port}")
    httpd.serve_forever()

def main():
    # Attempt to remove write protection

    if is_admin():
        # Your code that requires administrative privileges goes here
        if not remove_write_protection():
            return

        # Read from USB and get mount point
        mount_point = read_usb()

        print("Files on USB drive:")
        list_files(mount_point)

        # Encrypt all files on the USB drive
        encrypt_all_files(mount_point)

        # Example: Delete a suspicious file
        suspicious_file = os.path.join(mount_point, "suspicious_file.txt")
        if os.path.exists(suspicious_file):
            delete_file(suspicious_file)

        # Serve the USB drive content via HTTP
        host = socket.gethostbyname(socket.gethostname())  # Get the IPv4 address of the host machine
        serve_thread = threading.Thread(target=serve, args=(mount_point, host, 8000))
        serve_thread.start()

        # Wait for server thread to finish (not necessary if you want the script to continue running)
        serve_thread.join()

        # Unmount the USB device after manipulation
        os.system(f"umount {mount_point}")
    else:
        # Re-run the program with admin rights
        print("Requesting admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    if not remove_write_protection():
        return

    # Read from USB and get mount point
    mount_point = read_usb()
    
    print("Files on USB drive:")
    list_files(mount_point)
    
    # Encrypt all files on the USB drive
    encrypt_all_files(mount_point)

    # Example: Delete a suspicious file
    suspicious_file = os.path.join(mount_point, "suspicious_file.txt")
    if os.path.exists(suspicious_file):
        delete_file(suspicious_file)

    # Serve the USB drive content via HTTP
    host = socket.gethostbyname(socket.gethostname())  # Get the IPv4 address of the host machine
    serve_thread = threading.Thread(target=serve, args=(mount_point, host, 8000))
    serve_thread.start()

    # Wait for server thread to finish (not necessary if you want the script to continue running)
    serve_thread.join()

    # Unmount the USB device after manipulation
    os.system(f"umount {mount_point}")

if __name__ == "__main__":
    main()
