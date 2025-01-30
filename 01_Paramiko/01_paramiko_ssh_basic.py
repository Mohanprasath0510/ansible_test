import time
from paramiko import client
#paramiko: A Python library used for SSH communication. It provides tools to connect to remote servers and execute commands securely.
#client: The module within Paramiko that allows us to create an SSH client.

from getpass import getpass
#getpass: A standard library in Python used to securely input passwords without displaying them on the screen.


hostname = '192.168.17.2'
#hostname: The IP address or domain name of the remote device you want to connect to via SSH.

username = input("Enter username:")

if not username:
    username = "admin"
    print(f"username not provided, consider to default usernmae {username}")

password = getpass(f"Enter Password of the user {username}: ") or 'admin'
#getpass(): Prompts the user to input their password securely (input is not displayed to the screen).

ssh_client =client.SSHClient()
#ssh_client: A variable to hold the SSH client object.
#client.SSHClient(): Creates an instance of SSHClient from the paramiko library, which is used to manage the SSH connection.

ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
#set_missing_host_key_policy(): Specifies how the SSH client should handle unknown host keys.
#AutoAddPolicy(): Policy for automatically adding the hostname and new host key to the local


ssh_client.connect(hostname=hostname, 
                   username=username, 
                   password=password, 
                   look_for_keys=False, #Using "look_for_keys=False" forces Paramiko to use password authentication only.
                   allow_agent=False)   #Setting allow_agent=False ensures that Paramiko does not attempt key-based authentication via an SSH agent.
                                        #Similarly, SSH agents (allow_agent=True by default) store keys for passwordless authentication.

print("CONNECTED SUCCESSFULLY...")

device_access = ssh_client.invoke_shell() 
#ssh_client.invoke_shell(): creates an interactive shell session, similar to manually logging into a device via PuTTY or a terminal.

device_access.send("terminal length 0\n") #This command configures the terminal to display all the output without breaking it into pages.
device_access.send("show run\n") #send(): send the data to channel
time.sleep(5) #This command pauses the execution of the script for 5 seconds.

output = device_access.recv(35565) #recieve the datas are bytecode(35565)
print(output.decode()) #decode(): output convert to human understandable format

ssh_client.close() #close the ssh connection


