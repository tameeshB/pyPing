# chat_server.py
 
import sys, socket, select
import globals
import pypingcli.util
HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009#globals.port
def test():
    # globals.state['connected'] = True
    print("globals.state['connected']",globals.state['connected'])
def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
    print "Chat server started on port " + str(PORT)
    clientName = None
    pubKey = False
    sslEstablished = False

    while 1:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select([sys.stdin] + SOCKET_LIST,[],[])
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                # print "Client (%s, %s) connected" % addr
                # broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
                sys.stdout.write('.{:=^10}> '.format(globals.user)); sys.stdout.flush()
            elif sock == sys.stdin:
                msg = sys.stdin.readline()
                broadcast(server_socket, sock, "\r" + '.{:=^10}> {}'.format(globals.user,msg))
                # sys.stdout.write('\r.{:=^10}> '.sformat(globals.user)); sys.stdout.flush()
            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        if sslEstablished:
                            broadcast(server_socket, sock, "\r" + data) #some leak here
                            sys.stdout.write('\r.{:=^10}> '.format(globals.user)); sys.stdout.flush()
                        elif not clientName:
                            if data[:4] == "/im:":
                                t_client_name = data[4:]
                                sys.stdout.write("\rConnection request from {}. Accept(y/n)?".format(t_client_name))
                                keyPress = pypingcli.util.getch()
                                if keyPress == 'y' or keyPress == '\n':
                                    clientName = t_client_name
                                    sys.stdout.write("\rConnected to '{}'\n".format(clientName))
                                    sock.send('/asymkey?:')
                                    continue
                                else:
                                    if sock in SOCKET_LIST:
                                        SOCKET_LIST.remove(sock)
                                    continue
                            else:
                                continue
                        elif not pubKey:
                            # print("notp",data)
                            if data[:9] == "/asymkey:":
                                pubKey = data[9:]
                                encSymmKey = globals.keyMgrInstance.getEncSymmKey(pubKey)
                                sys.stdout.write("Encryption Key handshake:\n\tPart one:\n\t\tRecieving asymmetric key for '{}'.".format(clientName))
                                pubKey = True
                                sys.stdout.write("\n\tPart two:\n\t\tTransmitting RSA encrypted AES256 symmetric key to '{}'.\n".format(clientName))
                                sock.send('/encsymmkey:{}'.format(encSymmKey))
                                continue
                            else:
                                continue
                        elif data == '/secureconn:':
                            sslEstablished = True
                            sys.stdout.write("\nEstablished secure connection with '{}'\n".format(clientName))
                            sock.send('/im:{}'.format(globals.user))
                            sys.stdout.write('.{:=^10}> '.format(globals.user)); sys.stdout.flush() 
                            continue
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
    if message[0] == '/' or message[1] == '/':
        return
    sys.stdout.write(message+"\033[K");sys.stdout.flush()
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

 