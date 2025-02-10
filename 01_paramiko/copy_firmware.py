from jnpr.junos import Device
from jnpr.junos.utils.fs import FS
from jnpr.junos.utils.sw import SW
from jnpr.junos.exception import ConnectError
import sys
import os

def get_device_connection(hostname, username, password):
    """Establish a connection to the Juniper device."""
    try:
        dev = Device(host=hostname, user=username, passwd=password)
        dev.open()
        return dev
    except ConnectError as err:
        print(f"Failed to connect to {hostname}: {err}")
        sys.exit(1)

def check_firmware_exists(target_dev, firmware_filename):
    """Check if the firmware file already exists in /var/tmp/."""
    firmware_path = f"/var/tmp/{firmware_filename}"
    try:
        cmd = f"file list {firmware_path}"
        response = target_dev.rpc.cli(cmd, format='text')
        if "No such file" in response.text:
            print(f"Firmware {firmware_filename} NOT found in /var/tmp/")
            return False
        print(f"Firmware {firmware_filename} already exists in /var/tmp/")
        return True
    except Exception as e:
        print(f"Error checking firmware file: {str(e)}")
        return False

def copy_firmware_pyez(target_dev, local_firmware_path):
    """Copy firmware from local system to Juniper switch using PyEZ FS.cp()."""
    firmware_filename = os.path.basename(local_firmware_path)
    remote_path = f"/var/tmp/{firmware_filename}"

    print(f"Copying {firmware_filename} from local system to {remote_path} on Juniper switch...")

    try:
        fs = FS(target_dev)
        fs.cp(from_path=local_firmware_path, to_path=remote_path)
        print("Firmware copied successfully using FS.cp()!")
    except Exception as e:
        print(f"Error copying firmware via PyEZ FS.cp(): {str(e)}")
        sys.exit(1)

def verify_firmware_integrity(target_dev, firmware_filename):
    """Verify if the firmware file is correctly copied by checking its MD5 checksum."""
    firmware_path = f"/var/tmp/{firmware_filename}"
    try:
        cmd = f"file checksum md5 {firmware_path}"
        response = target_dev.rpc.cli(cmd, format='text')
        print(f"MD5 Checksum of {firmware_filename}:")
        print(response.text)
    except Exception as e:
        print(f"Error verifying firmware integrity: {str(e)}")
        sys.exit(1)

def upgrade_firmware(target_dev, firmware_filename):
    """Install firmware and reboot the Juniper switch."""
    firmware_path = f"/var/tmp/{firmware_filename}"
    
    print(f"Upgrading firmware using {firmware_path}...")
    sw = SW(target_dev)

    try:
        sw.install(package=firmware_path, progress=True)
        print("Firmware installation completed. Rebooting the device...")
        target_dev.rpc.request_system_reboot()
        print("Reboot command sent. Device will restart shortly.")
    except Exception as e:
        print(f"Firmware upgrade failed: {str(e)}")
        sys.exit(1)


def main():
    """Main function to handle firmware upgrade and SLAX script copy using PyEZ FS.cp()."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    target_host = input("Enter target device hostname or IP: ")
    local_firmware_path = input("Enter local firmware file path (e.g., /home/ubuntu/jinstall-vqfx-10-f-18.1R1.9.tgz): ")

    # Extract filename from path
    firmware_filename = os.path.basename(local_firmware_path)

    target_dev = get_device_connection(target_host, username, password)

    # Check if firmware already exists on the Juniper switch
    if not check_firmware_exists(target_dev, firmware_filename):
        # Copy firmware from local system to Juniper switch using PyEZ FS.cp()
        copy_firmware_pyez(target_dev, local_firmware_path)

    # Verify firmware integrity
    verify_firmware_integrity(target_dev, firmware_filename)

    # Upgrade firmware
    upgrade_firmware(target_dev, firmware_filename)

    print("Firmware upgrade and SLAX script transfer completed successfully.")

if __name__ == "__main__":
    main()
