from socket import *
from time import *
import os
import re

HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
repon = {'data':ctime(),'os':os.name,'ls':str(os.listdir(os.curdir))}

while True:
     print 'Waiting for Connecting...'
     tcpCliSock, addr = tcpSerSock.accept()
     print 'Connecting from:', addr

     while True:
         data = tcpCliSock.recv(BUFSIZ)
         finder = re.match(r'ls dir\((.+)\)',data)
         if not data:
             break
         elif repon.get(data):
             tcpCliSock.send(repon[data])
         elif finder:
             print os.listdir(finder.group(1))
             tcpCliSock.send(str(os.listdir(finder.group(1))))
         else:
             tcpCliSock.send(str(data))
     tcpCliSock.close()
tcpSerSock.close()