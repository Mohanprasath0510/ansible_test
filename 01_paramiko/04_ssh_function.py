import time
from paramiko import client
#paramiko: A Python library used for SSH communication. It provides tools to connect to remote servers and execute commands securely.
#client: The module within Paramiko that allows us to create an SSH client.

from getpass import getpass
#getpass: A standard library in Python used to securely input passwords without displaying them on the screen.

username = input("Enter username:")

if not username:
    username = "admin"
    print(f"username not provided, consider to default usernmae {username}")

password = getpass(f"\U0001F511 Enter Password of the user {username}: ") or 'admin'
#getpass(): Prompts the user to input their password securely (input is not displayed to the screen).

s1_commands = ['conf t',
            'int loopback 0',
            'ip add 1.1.1.1 255.255.255.0',
            'end']
s2_commands = ['conf t',
            'int loopback 0',
            'ip add 2.2.2.2 255.255.255.0',
            'end']
def cisco_cmd_executor(hostname,commands):  #define the function "cisco_cmd_executor()" 
                                            #hostname – Likely a string representing the Cisco device's IP address or hostname.
                                            #commands – Expected to be a list of commands that will be executed on the Cisco device.

    print(F"CONNECTING TO THE DEVICE {hostname}...")
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

    print(F"CONNECTED TO THE DEVICE {hostname}")

    device_access = ssh_client.invoke_shell() 
    #ssh_client.invoke_shell(): creates an interactive shell session, similar to manually logging into a device via PuTTY or a terminal.

    device_access.send("terminal length 0\n") #This command configures the terminal to display all the output without breaking it into pages.

    for cmd in commands:
        device_access.send(f"{cmd}\n") #send(): send the data to channel
        time.sleep(1) #This command pauses the execution of the script for 5 seconds.
        output = device_access.recv(35565) #recieve the datas are bytecode(35565)
        print(output.decode(),end='') #decode(): output convert to human understand
                                    #Normally, print() adds a newline (\n) at the end of the output.
                                    #end='' removes that newline, so the next print() statement continues on the same line.

    device_access.send("sh run int loopback 0\n")
    time.sleep(1)
    output = device_access.recv(35565) #recieve the datas are bytecode(35565)
    print(output.decode()) #decode(): output convert to human understandable format

    ssh_client.close() #close the ssh connection

cisco_cmd_executor('192.168.17.2',s1_commands)     #'192.168.17.2' → The IP address of Switch S1, meaning the function will execute commands on this device.                                                   #s1_commands → A variable (likely a list) containing the commands to be executed on Switch S1.
cisco_cmd_executor('192.168.17.50',s2_commands)    #s1_commands → A variable (likely a list) containing the commands to be executed on Switch S1.
