# chat_client.py

import sys, socket, select, os
import globals
import pypingcli.util
from pypingcli.cryptoManager.keyManager import KeyManager

def chat_client(argHost=None):

    host = argHost if argHost is not None else pypingcli.util.safeInput(message="Enter host address to connect to.\n.>")
    port = int(globals.port)
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # states
    accepted = False
    symmkeyRecieved = False
    keyMgrInstance = KeyManager()
    sslEstablished = False
    remoteUserName = None
    # generate keys
    pubKey = None
    # print("1",keyMgrInstance.keyStatus())
    # keyMgrInstance.generateAsymKeys()
    # print("2",keyMgrInstance.keyStatus(),keyMgrInstance.pubKey)
    # if keyMgrInstance.keyStatus == 0:
        # print('ooo')
    pubKey = keyMgrInstance.generateAsymKeys()
        # print('pubKeyset',pubKey)
        # print(keyMgrInstance.keyStatus)
    # connect to remote host
    try :
        sys.stdout.write('Awaiting connection invitation response...')
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
    s.send('/im:{}'.format(globals.user))
    # print 'Connected to remote host. You can start sending messages'
    if host == globals.internetServerIP:
        print("/**\n\tCaution:\n\t\tThis is a public and unencrypted channel.\n\t\tAnyone online can read the messages sent here.\n **/")
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
                    if sslEstablished:
                        if data[:11]=='/ciphermsg:':
                            sys.stdout.write('\r.{:=^10}> {}'.format(remoteUserName,keyMgrInstance.decrypt(data[11:])))
                        else:
                            sys.stdout.write(data)
                        sys.stdout.write('.{:=^10}> '.format(globals.user)); sys.stdout.flush()
                    elif not accepted:
                        if data == "/asymkey?:":
                            accepted = True
                            sys.stdout.write('\nConnection invitation accepted.                 ')
                            sys.stdout.write('\nInitiating crypto handshake sequence...')
                            sys.stdout.write("\nEncryption Key handshake:\n\tPart one:\n\t\tTransmitting asymmetric key.\n")
                            s.send('/asymkey:{}'.format(pubKey))
                            continue
                        else:
                            continue
                    elif not symmkeyRecieved:
                        if data[:12] == '/encsymmkey:':
                            symmkeyRecieved = True
                            sys.stdout.write("\n\tPart two:\n\t\tRecieving and deciphering RSA encrypted AES256 symmetric key..\n")
                            symmKeyCipherText = data[12:]
                            if keyMgrInstance.decryptKey(symmKeyCipherText):
                                s.send('/secureconn:')
                            continue
                        else:
                            continue
                    elif not sslEstablished:
                        if data[:4] == "/im:":
                            sslEstablished = True
                            os.system('clear')
                            remoteUserName = data[4:]
                            sys.stdout.write("\nEstablished secure connection with '{}'\n".format(remoteUserName))
                            sys.stdout.write('.{:=^10}> '.format(globals.user)); sys.stdout.flush() 
                            continue

            else :
                if not sslEstablished:
                    continue
                # user entered a message
                msg = sys.stdin.readline()
                s.send('/ciphermsg:' + keyMgrInstance.encrypt(msg))
                sys.stdout.write('.{:=^10}> '.format(globals.user)); sys.stdout.flush() 

