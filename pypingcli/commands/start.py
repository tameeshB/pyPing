from json import dumps
from .base import Base
import globals
from os import path
import json
import sys

class Start(Base):
    
    def run(self):
        globals.state['start'] = True
        if not self.checkConfig():
            self.initConfig()
            globals.loadConfig()
        else:
            self.greet()

    def greet(self, new = False):
        if new:
            print "Hello, ",
        else:
            print "Welcome back, ",
        print(globals.user + "!")
    def checkConfig(self):
        """
        Checks if initialisation is done before
        """
        return path.exists(globals.configFile)
    
    def initConfig(self):
        """
        Config initialisation.
        """
        print("\tHi!"
               "\n\tThank you for installing pyPing."
               "\n\tIf I'm not wrong, this is the first run of this program."
                "\n\tPlease enter required information for initialising the program.\n")
        config = {}
        try:
            maxTries = 3
            while maxTries:
                tmpInput = None
                try:
                    tmpInput = raw_input('Please enter desired username: ')
                except SyntaxError:
                    print("\n\tBlank input.")
                if tmpInput and len(tmpInput)>5:
                    config['user'] = tmpInput
                    break
                else:
                    print("\n\tName too short.")
                maxTries -= 1
            else:
                print("\n\tInvalid input.")
                sys.exit(1)
            # init crypto keys
        except KeyboardInterrupt:
            print("\n\tExit by user interrupt.")
            sys.exit(1)
        except EOFError:
            print("\n\tExit by user interrupt.")
            sys.exit(1)
        
        with open(globals.configFile, 'w') as configFile:
            json.dump(config, configFile)

        