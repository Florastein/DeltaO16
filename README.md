Get started by customizing your environment (defined in the .idx/dev.nix file) with the tools and IDE extensions you'll need fo# USB Drive Encryption and File Serving

This Python script provides functionalities to encrypt files on a USB drive using AES-256 encryption and serve them over HTTP with basic authentication. It allows secure manipulation and access of files stored on a USB drive connected to your computer.

## Features

- **Encryption**: Encrypts all files on the USB drive using AES-256 encryption.
- **Decryption**: Decrypts encrypted files back to their original state.
- **File Deletion**: Allows deletion of specific files from the USB drive.
- **HTTP Server**: Serves the files on the USB drive over HTTP, enabling remote access.
- **Basic Authentication**: Implements basic authentication to restrict access to authorized users only.

## Prerequisites

- Python 3.x installed on your system.
- `pycryptodome` library installed (`pip install pycryptodome`).
- `pyusb` library installed (`pip install pyusb`)

## Usage

1. **Setup**
   - Connect the USB drive to your computer.
   - Ensure the USB drive is mounted correctly (e.g., `/mnt/usb`).

2. **Run the Script**
   - Open a terminal.
   - Navigate to the directory containing the script (`DeltaO16.py`).
   - Run the script using Python: `python DeltaO16.py`.

3. **Operations**
   - Follow the on-screen instructions to remove write protection, list files, encrypt/decrypt files, delete specific files, and serve files over HTTP.

4. **HTTP Server Access**
   - Once the script starts serving files, access them using a web browser:
     - URL: `http://<host_ip>:8000`
     - Username: `user`
     - Password: `password`
   - Replace `<host_ip>` with the IPv4 address of the host machine.

5. **Security**
   - For enhanced security, consider using HTTPS with SSL/TLS certificates if deploying the server in a production environment.

6. **Cleanup**
   - After use, safely eject or unmount the USB drive from your computer.

## Notes

- This script provides basic functionalities and should be used responsibly.
- Ensure you have backups of important data before encryption or deletion operations.
- Modify the `username` and `password` in the script (`AuthHandler` class) to suit your security requirements.

## License

This script is provided under the [KTU License]0420221297D and 0420221201D
