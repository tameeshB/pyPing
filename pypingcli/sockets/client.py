#!/usr/bin/env python3

import socket

class Client(object):
    def __init__(self):
        # load additional Python modules
        import socket  
        import time

        # create TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # retrieve local hostname
        local_hostname = socket.gethostname()

        # get fully qualified hostname
        local_fqdn = socket.getfqdn()

        # get the according IP address
        ip_address = socket.gethostbyname(local_hostname)

        # bind the socket to the port 23456, and connect
        server_address = (ip_address, 23456)  
        sock.connect(server_address)  
        print ("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

        # define example data to be sent to the server
        temperature_data = ["15", "22", "21", "26", "25", "19"]  
        for entry in temperature_data:  
            print ("data: %s" % entry)
            new_data = str("temperature: %s\n" % entry).encode("utf-8")
            sock.sendall(new_data)

            # wait for two seconds
            time.sleep(2)

        # close connection
        sock.close()  