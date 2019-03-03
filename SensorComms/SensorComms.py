#!/usr/bin/env python

import time
import socket
import os
import sys

#On the slate device Fedora Core 25), I did a sudo bluetoothctl and 
#did a trust <RPI MAC ADDRESS>, and it seemed to connect after that.
#I also did a connect <RPI MAC ADDRESS>, but I don't think that is what
#made it work.

displayDebugMessages=False

if len(sys.argv) > 1 and sys.argv[1]  == 'debug':
    displayDebugMessages=True
def DBG(msg):
    if displayDebugMessages:
        print(msg)

#set use_bluetooth to False to use 802.11
use_bluetooth=True

#The hciconfig can be run on the pi to display it's bluetooth MAC address.
thisdir=os.path.dirname(os.path.abspath(__file__))

if use_bluetooth is False:
    pollinginterval = 5
else:
    pollinginterval=2.5

while True:
    data = None
    with open(os.path.join(thisdir, 'HelmetList.txt'), 'r') as f:
        data = f.read()

    for line in data.splitlines():
        if len(line) == 0:
            continue
        
        if line[0] == '#':
            continue

        #DBG('\n\nTEST line = %s'%line)

        serverMacAddress, port, playerInfo = line.split(',')
        DBG('serverMacAddress = %s, port = %s, playerInfo = %s'%(serverMacAddress, port, playerInfo))
        s = None
        if use_bluetooth is True:
            s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.settimeout(5)
        port = int(port)
        DBG('Calling s.connect(%s, %d)'%(serverMacAddress,port))
        try:
            DBG("calling s.connect")
            s.connect((serverMacAddress,port))

            DBG("calling s.recv")
            stats = s.recv(512).split(',')
            #print('%s: Heartrate = %s, Temperature = %s'%(playerInfo, stats[0], stats[1]))
            f = open("/var/www/html/tmp/playerlist.txt", "w")
            if f:
                #print("hi")
                f.write("%s,%s,%s"%(playerInfo,stats[0],stats[1]))
                f.close()
        
        except Exception as e:
            DBG('Connection failed')
            s.close()
    DBG('Sleeping for %d seconds'%pollinginterval)
    time.sleep(pollinginterval) 

