"""
pyPingCLI
 
Usage:
  pyping start
  pyping resume --username <username>
  pyping -h | --help
  pyping --version
 
Options:
  -h --help                         Show this screen.
  --version                         Show version.
 
Examples:
  pyping start
 
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/tameeshB/pyPingCLI
"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION
from commands.prompts import invokePrompt
from pypingcli.sockets.util import startDaemonServer
import os
import sys
import globals

# use prompt-toolkit
def main():
    """Main CLI entrypoint."""
    import commands
    globals.init()
    globals.loadConfig()
    os.system('clear')
    options = docopt(__doc__, version=VERSION)
    # print(options)
    try:
        for k, v in options.iteritems():
            if hasattr(commands, k):
                module = getattr(commands, k)
                commands = getmembers(module, isclass)
                command = [command[1] for command in commands if command[0] != 'Base'][0]
                command = command(options)
                command.run()
        # startDaemonServer()
        while invokePrompt() != -1:
            pass
    except KeyboardInterrupt:
        print("\nProgram ended by user keyboard interrupt.\n")
    sys.exit(0)
    
    
