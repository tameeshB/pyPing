import globals
import sys
from pypingcli import sockets
from pypingcli.messaging.socketAction import sendMsg
def invokePrompt():
    """State based prompt calls."""
    commands = []
    if globals.state['connected'] == True:
        commands = ['send','disconnect']
        run = printPrompt(commands)
        if run == -1:
            return -1
        elif run == "send":
            sendMsg()
        
    else:
        commands = ['connect','edit username','ping IP','my IP']
        run = printPrompt(commands)
        if run == -1:
            return -1
        elif run == "connect":
            sockets.Client()
        elif run == "accept":
            sockets.Server()



def printPrompt(options):
    """Prints, validates and returns options."""
    print "Commands : 0) Quit ",
    for index,command in enumerate(options,1):
        print "{}){} ".format(index,command) ,
    invFlag = True
    while invFlag:
        tmpInput = None
        try:
            tmpInput = int(input("\n: "))
        except:
            pass
        if tmpInput >= 0 and tmpInput<=len(options):
            break
        print("Invalid Option.")
        
    if tmpInput == 0:
        return -1
    return options[tmpInput-1]