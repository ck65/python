from socket import *

Host = '127.0.0.1'
Port = 21456
Addr = (Host, Port)
client = socket(AF_INET, SOCK_DGRAM)

while True:

    data = raw_input('> ')
    if not data:
        break
    client.sendto(data, Addr)
    data = client.recvfrom(1024)
    print data

print getservbyname("daytime", 'udp')
client.close()