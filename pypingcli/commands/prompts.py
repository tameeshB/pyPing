import globals
import sys
from pypingcli import sockets

def invokePrompt():
    """State based prompt calls."""
    commands = []
    if globals.state['connected'] == True:
        pass
    else:
        commands = ['connect','accept','edit username','ping IP','my IP']
        run = printPrompt(commands)
        if run == "connect":
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
        sys.exit(0)
    return options[tmpInput-1]