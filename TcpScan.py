#!/usr/bin/env python
# encoding: utf-8
# @Time: 2018/9/24 20:59

#!/usr/bin/env python
# encoding: utf-8
# @Time: 2018/9/24 20:59

import optparse
from socket import *
from threading import *
screenLock = Semaphore(value=1)
def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET,SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print '[+]%d/tcp open' % tgtPort
        print '[+] ' + str(results)
    except:
        screenLock.acquire()
        print '[+]%d/tcp closed' % tgtPort
    finally:
        screenLock.release()
        connSkt.close()
def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print '[-] Cannot resolve %s : Unknown host'%tgtHost
        return
    try:
        tgtname = gethostbyaddr(tgtIP)
        print '\n[+] Scan Results for: '+ tgtname[0]
    except:
        print '\n[+] Scan Results for: '+ tgtIP
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()
def main():
    # type: () -> object
    parser = optparse.OptionParser('Usage%prog -H <tgthost> -p <tgtport>')
    parser.add_option('-H', dest='tgthost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtport', type='string', help='specify target port')
    (options,args) = parser.parse_args()
    tgtHost = options.tgthost
    tgtPorts = str(options.tgtport).split(', ')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print parser.usage
        exit(0)
    portScan(tgtHost, tgtPorts)

if __name__ == "__main__":
    main()