from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.start_shell import StartShell
 
def precheck(ip, username, password):
    try:
        print(f"Performing precheck on {ip}...")
 
        # Connect to the Junos device
        dev = Device(host=ip, user=username, passwd=password)
        dev.open()
 
        # Create/Open a text file to save the output
        with open(f"precheck_output_{ip}.txt", "w") as file:
            file.write(f"Precheck Results for {ip}\n")
            file.write("=" * 50 + "\n\n")
 
            precheck_commands = [
                "show ethernet-switching table",
                "show version",
                "show interfaces terse",
                "show interfaces descriptions",
                "show lldp neighbors",
                "show virtual-chassis"
            ]
 
            # Execute commands and save output
            for command in precheck_commands:
                response = dev.cli(command, warning=False)
                # Print to console
                print(f"\nOutput for '{command}':\n{response}")
                # Write to file
                file.write(f"Output for '{command}':\n")
                file.write(response)
                file.write("\n" + "-" * 50 + "\n")
 
        dev.close()
        print(f"\nPrecheck completed on {ip}. Output saved to 'precheck_output_{ip}.txt'.")
 
    except ConnectError as e:
        print(f"Error: Unable to connect to {ip}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
 
# Example usage
if __name__ == "__main__":
    device_ip = "192.168.17.143"   # Replace with the Junos switch IP
    username = "admin"             # Replace with the correct username
    password = "juni123"           # Replace with the correct password
    precheck(device_ip, username, password)