# globals.py

from os.path import abspath, dirname, join
from os import path
import json

def init():
    global thisDir
    global configFile
    global user
    global state
    global port
    global internetServerIP
    thisDir = abspath(dirname(__file__))
    configFile = join(thisDir, 'config.json')
    user = None
    internetServerIP = '35.200.238.63'
    state = {
        'connected' : False,
        'start' : False,
        'connecting' : False,
        'sending' : False,
        'listening' : False,
        'pinging' : False
    }
    port = 9009
    

def loadConfig():
    global user
    global configFile
    if path.exists(configFile):
        with open(configFile) as jsonConfigData:
            data = json.load(jsonConfigData)
        user = data['user']
    
