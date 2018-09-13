#!/usr/bin/env python3

import socket
import globals
from pypingcli.messaging.socketAction import action
from pypingcli.sockets.client import Client

class Server(object):
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', 23456)  
        sock.bind(server_address)
        sock.listen(1)
        while True:
            # wait for a connection
            connection, client_address = sock.accept()
            try:
                # show who connected to us
                print ('connection from ', client_address)
                Client(client_address[0])
                globals.state["connected"] = True
                # receive the data in small chunks and print it
                while True:
                    data = connection.recv(64)
                    if data:
                        # print("recv:",data)
                        connection.sendall(action(data))
                    else:
                        # connection.sendall(action(data))
                        break
            finally:
                # Clean up the connection
                connection.close()