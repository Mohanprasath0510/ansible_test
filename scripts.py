import paramiko
import getpass
import time
import json
import re  # Import regex module
def establish_ssh_connection(hostname, username, password):
    """
    Establish an SSH connection to the device.
    Args:
        hostname (str): The hostname or IP address of the device.
        username (str): The username to use for the SSH connection.
        password (str): The password to use for the SSH connection.
    Returns:
        paramiko.SSHClient: The established SSH connection.
    """
    print(f"Connecting to {hostname}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    print(f"Connected to {hostname}.")
    return ssh
def execute_command(ssh, command):
    """
    Execute a command on the device and return the output.
    Args:
        ssh (paramiko.SSHClient): The established SSH connection.
        command (str): The command to execute.
    Returns:
        tuple: A tuple containing the command output and error messages.
    """
    stdin, stdout, stderr = ssh.exec_command(command)
    time.sleep(1)  # Allow command execution time
    # return stdout.read().decode('utf-8').strip(), stderr.read().decode('utf-8').strip()  #.strip()
    # Read output and error messages
    output = stdout.read().decode('utf-8').strip()
    error = stderr.read().decode('utf-8').strip()
    # Remove lines containing only "-------------------------------------------"
    cleaned_output = "\n".join(
        line for line in output.splitlines() if not re.match(r"^-{5,}$", line)
    )

    return cleaned_output, error

def save_output_to_file(filename, data): #data (dict): The command output to save in JSON format.
    """
    Save command output to a file.
    Args:
        filename (str): The filename to save the output to.
        output (str): The command output to save.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
# json.dump(): This function serializes (converts) a Python dictionary into a JSON format and writes it directly to a file.
# data: This is the Python dictionary containing the data you want to save.
# file: This is the file object where the JSON data will be written.
# indent=4: This makes the JSON human-readable by adding 4 spaces per indentation level.
def main():
    # Input details
    hostname = input("Enter the target client hostname: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    pre_check_commands = [
        "show ethernet-switching table",
        "show version",
        "show interfaces terse",
        "show interfaces descriptions",
        "show lldp neighbors",
        "show virtual-chassis"
    ]
    try:
        # Step 1: Establish SSH Connection
        ssh = establish_ssh_connection(hostname, username, password)
        # Step 2: Pre-Checks
        print("Performing pre-checks...")
        pre_check_data = {}  #if use "" for output as a string 
        for command in pre_check_commands:
            output, error = execute_command(ssh, command)
            if error:
                print(f"Error executing command: {command}\n{error}")
                pre_check_data[command] = {"error": error}   # line check
            else:
                pre_check_data[command] = {"output": output}  # line check
        # Save output to JSON file
        save_output_to_file("pre_check.json", pre_check_data)
        print("Pre-checks completed and saved to pre_check.json.")

        # Close SSH connection
        ssh.close()
        print("SSH connection closed.")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    main()