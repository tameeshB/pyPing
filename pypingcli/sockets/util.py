import socket
import threading 
import os
from pypingcli.sockets import Server

def getSelfIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIPAddr = s.getsockname()[0]
    s.close()
    return localIPAddr

def startDaemonServer():
    t1 = threading.Thread(target=Server, name='t1')
    t1.daemon = True
    t1.start() 
    