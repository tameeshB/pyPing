# chat_client.py

import sys, socket, select
import globals
import pypingcli.util

def chat_client():

    host = pypingcli.util.safeInput(message="Enter host address to connect to.\n.>")
    port = int(globals.port)
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('.{:=^10}> '.format(globals.user)); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('.{:=^10}>s '.format(globals.user)); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send('.{:=^10}> {}'.format(globals.user,msg))
                sys.stdout.write('.{:=^10s}> '.format(globals.user)); sys.stdout.flush() 

