import socket, select
import re

server = socket.socket()
Addr = ("", 2050)
server.bind(Addr)
server.listen(5)
inputs = [server]
clientdict = {}
user = "No name user"
roomnumber = 0
print "Start the chat server..."

while True:
    rs, ws, es = select.select(inputs, [], [])
    for i in rs:
        if i == server:
            client, addr = i.accept()
            # print "Connected from",addr,"this is user%s"%user
            inputs.append(client)
            clientdict[client] = [client, addr, user, roomnumber]

        else:
            try:
                data = i.recv(1024)
                matchname = re.match(r'(.+)\sjoin the server', data)
                matchroom = re.match(r'Join the room(\d)', data)
                if matchname:
                    print data
                    for x in inputs:
                        if x == server or x == i:
                            pass
                        else:
                            if clientdict[x][2] == "No name user" or clientdict[x][3] == 0:
                                pass
                            else:
                                x.send(data)
                    username = matchname.group(1)
                    clientdict[i][2] = username
                    i.send('Welcome,%s' % username)
                elif matchroom:
                    print '%s' % clientdict[i][2], data
                    roomnumber = matchroom.group(1)
                    clientdict[i][3] = roomnumber
                    i.send('You join room%s' % roomnumber)
                    for x in inputs:
                        if x == server or x == i:
                            pass
                        else:
                            if clientdict[x][3] == clientdict[i][3]:
                                x.send('%s join this room' % clientdict[i][2])
                else:
                    senddata = "%s said:%s" % (clientdict[i][2], data)
                    for x in inputs:
                        if x == server or x == i:
                            pass
                        else:
                            if clientdict[x][3] == clientdict[i][3]:
                                x.send(senddata)
                disconnected = False

            except socket.error:
                disconnected = True

            if disconnected:
                leftdata = "%s has left" % clientdict[i][2]
                print leftdata
                for x in inputs:
                    if x == server or x == i:
                        pass
                    else:
                        x.send(leftdata)
                inputs.remove(i)
