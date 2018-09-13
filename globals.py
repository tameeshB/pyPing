# globals.py

from os.path import abspath, dirname, join
import json

def init():
    global thisDir
    global configFile
    global user
    global state
    thisDir = abspath(dirname(__file__))
    configFile = join(thisDir, 'config.json')
    user = None
    state = {
        'connected' : False,
        'start' : False,
        'connecting' : False,
        'sending' : False,
        'listening' : False,
        'pinging' : False
    }

def loadConfig():
    global user
    with open(configFile) as jsonConfigData:
        data = json.load(jsonConfigData)
    user = data['user']
    
