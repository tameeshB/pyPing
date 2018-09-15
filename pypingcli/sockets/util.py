import socket
import threading 
import os
import globals
from time import sleep
# from pypingcli.sockets import Server

def getSelfIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIPAddr = s.getsockname()[0]
    s.close()
    return localIPAddr

def test2(stateDict):
    k = 0
    while True:
        if stateDict["connected"]== 't':
            return
        stateDict["connected"] = k
        sleep(2)
        k+=1

def startDaemonServer():
    t1 = threading.Thread(target=test2, name='t1',args=[globals.state])
    t1.daemon = True
    t1.start() 
    return t1
    