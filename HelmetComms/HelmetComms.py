#!/usr/bin/env python

#The hciconfig can be run on the pi to display it's bluetooth MAC address.

import time
import socket
import os
import sys

#install pybluez..sudo apt-get install pybluez
import bluetooth

displayDebugMessages=False

if len(sys.argv) > 1 and sys.argv[1]  == 'debug':
    displayDebugMessages=True
    

def DBG(msg):
    if displayDebugMessages:
        print(msg)

#set use_bluetooth to False to use 802.11
use_bluetooth=True

if use_bluetooth is True:
    use_pybluez = False

from subprocess import Popen, PIPE

thisdir=os.path.dirname(os.path.abspath(__file__))

if use_bluetooth is True:
    #if use_pybluez is True:
        #devices = bluetooth.discover_devices()
        #for device in devices:
        #    print('Device = %s'%str(device))
    p = Popen('hciconfig | grep BD', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    outstr = str(p.stdout.read())
    hostMacAddress = outstr.split(' ')[2]
    port = 1
else:
    hostMacAddress = '192.168.1.147'
    port=50000


backlog = 5
size = 1024

s = None
if use_bluetooth is True:
    if use_pybluez is False:
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    else:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        hostMacAddress=""
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DBG('Calling s.bind(%s, %d)'%(hostMacAddress, int(port)))
s.bind((hostMacAddress,port))
#if use_bluetooth is False:
s.listen(backlog)
#else:
#s.listen(1)

while True:
    DBG('Calling accept')
    client, address = s.accept()
    DBG('Returned from accept')
    try:
        heartrate = None
        bodytemp = None
        with open(os.path.join(thisdir, 'Heartrate.txt'), 'r') as f:
            heartrate = f.read().rstrip()
        with open(os.path.join(thisdir, 'Bodytemp.txt'), 'r') as f:
            bodytemp = f.read().rstrip()
        stats = '%s,%s'%(heartrate, bodytemp)
        #DBG('Sending stats %s'%stats)
        bytessent = client.send(bytes(stats, 'UTF-8'))
        DBG('Sent %d bytes'%bytessent)
        #data = client.recv(size)
        
    except:
        print('Closing socket')
        client.close()
        s.close()
        #break
    #sleeptime=5
    #DBG('Sleeping %d seconds'%sleeptime)
    #time.sleep(sleeptime)

