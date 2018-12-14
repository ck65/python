from socket import *
import threading
from time import sleep

HOST = 'localhost'
PORT = 2050
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
username = raw_input("Please set your username:")
tcpCliSock.send("%s join the server" % username)
data = tcpCliSock.recv(BUFSIZ)
print data
room = raw_input("Input room number(Input a number 1-9):")
tcpCliSock.send("Join the room%s" % room)
data = tcpCliSock.recv(BUFSIZ)
print data


def send():
    while True:
        data = raw_input(' > ')
        if not data:
            continue
        else:
            tcpCliSock.send(data)


def receive():
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        print data
        print ' > ',


t1 = threading.Thread(target=send)
t2 = threading.Thread(target=receive)
t1.start()
t2.start()
t1.join()
t2.join()

tcpCliSock.close()
