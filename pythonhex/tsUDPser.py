from socket import *

Host = ''
Port = 21456
ADDR = (Host, Port)

s = socket(AF_INET, SOCK_DGRAM)
s.bind(ADDR)

while True:
    print 'waiting for connecting'
    data, addr = s.recvfrom(1024)
    print addr
    print data

# noinspection PyUnreachableCode
s.close()
