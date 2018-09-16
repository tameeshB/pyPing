# chat_server.py
 
import sys, socket, select, os
import globals
import pypingcli.util
HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009 # globals.port
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
    # state and data storages
    clientName = None
    pubKey = False
    sslEstablished = False

    while 1:
        ready_to_read,ready_to_write,in_error = select.select([sys.stdin] + SOCKET_LIST,[],[])
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                sys.stdout.write('\r.{:=^10}> '.format(globals.user)); sys.stdout.flush()
            elif sock == sys.stdin:
                msg = sys.stdin.readline()
                broadcast(server_socket, sock, msg)
            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        if sslEstablished:
                            if data[:11]=='/ciphermsg:':
                                sys.stdout.write('\r.{:=^10}> {}'.format(clientName,globals.keyMgrInstance.decrypt(data[11:])))
                            else:
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
                            os.system('clear')
                            sys.stdout.write("\nEstablished secure connection with '{}'\n".format(clientName))
                            sock.send('/im:{}'.format(globals.user))
                            sys.stdout.write('.{:=^10}> '.format(globals.user)); sys.stdout.flush() 
                            continue
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()

# @todo
def broadcast(server_socket, sock, message):
    if (len(message)>0 and message[0] == '/') or (len(message)>1 and message[1] == '/'):
        return
    # sys.stdout.write('\r.{:=^10}><> {}'.format(globals.user,message));sys.stdout.flush()
    sys.stdout.write('\r.{:=^10}> '.format(globals.user)); sys.stdout.flush()
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send('/ciphermsg:' + globals.keyMgrInstance.encrypt(message))
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

 