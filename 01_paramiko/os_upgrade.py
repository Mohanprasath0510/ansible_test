from jnpr.junos import Device
from jnpr.junos.utils.fs import FS
from jnpr.junos.utils.sw import SW
from jnpr.junos.exception import ConnectError
import time
import sys

def get_device_connection(hostname, username, password):
    try:
        dev = Device(host=hostname, user=username, passwd=password)
        dev.open()
        return dev
    except ConnectError as err:
        print(f"Failed to connect to {hostname}: {err}")
        sys.exit(1)

# def run_command(dev, command):
#     return dev.rpc.cli(command, format='text')
def run_command(dev, command):
    """Run CLI command and ensure output is always a string."""
    try:
        output = dev.rpc.cli(command, format='text')
        if output is None:
            return f"Command '{command}' returned no data."
        return output.text if hasattr(output, 'text') else str(output)
    except Exception as e:
        return f"Error executing {command}: {str(e)}"

def save_output(output, filename):
    with open(filename, "w") as f:
        f.write(output)

def check_redundant_status(redundant_dev):
    status = run_command(redundant_dev, "show virtual-chassis")
    print(status)
    return "Yes" in input("Is the redundant device stable? (Yes/No): ")

def pre_checks(target_dev):
    commands = [
        "show ethernet-switching table",
        "show version",
        "show interface terse",
        "show interface descriptions",
        "show lldp neighbors",
        "show virtual-chassis"
    ]
    # output = "\n".join([run_command(target_dev, cmd) for cmd in commands])
    output = "\n".join(str(run_command(target_dev, cmd)) for cmd in commands)
    save_output(output, "pre_check_output.txt")
    return "Yes" in input("Proceed with upgrade? (Yes/No): ")

def verify_firmware(target_dev, firmware_list):
    fs = FS(target_dev)
    missing_files = [fw for fw in firmware_list if not fs.isfile(f"/var/tmp/{fw}")]
    if missing_files:
        print(f"Missing firmware files: {missing_files}")
        # Assume files are copied manually or through SCP

def upgrade_firmware(target_dev, firmware_list):
    sw = SW(target_dev)
    for firmware in firmware_list:
        print(f"Upgrading to {firmware}...")
        sw.install(package=f"/var/tmp/{firmware}", progress=True)
        print("Rebooting device...")
        target_dev.reboot()
        time.sleep(300)

def post_checks(target_dev):
    commands = [
        "show ethernet-switching table",
        "show version",
        "show interface terse",
        "show interface descriptions",
        "show lldp neighbors",
        "show virtual-chassis"
    ]
    output = "\n".join(str(run_command(target_dev, cmd)) for cmd in commands)
    save_output(output, "post_check_output.txt")

def compare_results():
    with open("pre_check_output.txt") as pre, open("post_check_output.txt") as post:
        pre_data = pre.readlines()
        post_data = post.readlines()
        diff = [line for line in post_data if line not in pre_data]
    save_output("\n".join(diff), "comparison_output.txt")

def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    target_host = input("Enter target upgrade device hostname: ")
    firmware_list = input("Enter firmware list (comma-separated): ").split(",")

    target_dev = get_device_connection(target_host, username, password)
    
    if not pre_checks(target_dev):
        print("Pre-checks failed. Aborting upgrade.")
        sys.exit(1)
    
    verify_firmware(target_dev, firmware_list)
    upgrade_firmware(target_dev, firmware_list)
    post_checks(target_dev)
    compare_results()
    print("Upgrade completed successfully.")

if __name__ == "__main__":
    main()
