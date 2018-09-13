#!/usr/bin/env python3

import socket

class Server(object):
    def __init__(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(s.getsockname()[0])
        s.close()
        # create TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the port 23456
        server_address = ('', 23456)  
        print ('starting up on %s port %s' % server_address)  
        sock.bind(server_address)

        # listen for incoming connections (server mode) with one connection at a time
        sock.listen(1)

        while True:  
            # wait for a connection
            print ('waiting for a connection')
            connection, client_address = sock.accept()

            try:
                # show who connected to us
                print ('connection from', client_address)

                # receive the data in small chunks and print it
                while True:
                    data = connection.recv(64)
                    if data:
                        # output received data
                        print ("Data: %s" % data)
                    else:
                        # no more data -- quit the loop
                        print ("no more data.")
                        break
            finally:
                # Clean up the connection
                connection.close()