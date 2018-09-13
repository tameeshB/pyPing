#!/usr/bin/env python3

import socket
import json
import globals
from pypingcli.messaging.socketAction import action
class Client(object):
    def __init__(self, ip = None):
        # load additional Python modules
        import socket  
        import time

        # create TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip == None:
            ip_address = raw_input('Enter IP(IPv4) to connect to: ')
        else:
            ip_address = ip_address
        server_address = (ip_address, 23456)  
        sock.connect(server_address)  
        print ("connecting to %s" % (ip_address))
        init = json.dumps({'e':'name','dir':'get'})
        sock.sendall(init)
        time.sleep(2)
        init = json.dumps({'e':'name','dir':'post','d':globals.user})
        sock.sendall(init)
        time.sleep(2)
        init = json.dumps({'e':'msg','d':"Hi!"})
        sock.sendall(init)
        # sock.sendall(init)
        # while True
        # define example data to be sent to the server
        # temperature_data = ["15", "22", "21", "26", "25", "19"]  
        # for entry in temperature_data:  
        #     print ("data: %s" % entry)
        #     new_data = str("temperature: %s\n" % entry).encode("utf-8")
        #     sock.sendall(new_data)

        #     # wait for two seconds
        #     time.sleep(2)

        # # close connection
        sock.close()  