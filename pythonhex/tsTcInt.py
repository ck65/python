from socket import *

Host = '127.0.0.1'
Port = 21567
ADDR = (Host, Port)

client1 = socket(AF_INET, SOCK_STREAM)
client1.connect(ADDR)

while True:
    data = raw_input('> ')
    if not data:
        continue
    client1.send(data)
    data = client1.recv(1024)
    if not data:
        continue
    print data

client1.close()