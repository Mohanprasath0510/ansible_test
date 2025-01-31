#------------------convert byte to string---------------------

b1= b"\n\n hi\tiam Mohan" #b1 is var name, And b""-given the data to byte format.
print(b1)
print(type(b1))
print(b1.decode()) #decode(): convert to human readable format.



#------------------convert string to byte---------------------

intro_str = ''' 
Hello,
My name is Mohan prasath, 
and I am a Network Automation Developer with expertise in enterprise networking and security. 
I have 6 months of experience in network infrastructure, specializing in routing, switching, firewall configurations, and network automation.
'''
print(intro_str.encode()) #encode(): convert the output to bytes


#------------------how to use emojis---------------------

byte_emoji = b"\xF0\x9F\x98\x89"
unicode_emoji = "\U0001F609" #"U+1F609": unicode default char is "8" but we have a "5"(U+ 1F609) char, so add "3"(000) char like as "\U0001F609"
print(byte_emoji.decode())
print(unicode_emoji)
