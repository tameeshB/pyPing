import re

def safeInput(message = "",**kwargs):
    tries = 1 if "tries" not in kwargs.keys() else kwargs["tries"]
    returnVal = None
    while tries >0:
        try:
            returnVal = raw_input(message)
        except:
            pass
        if len(returnVal)>0:
            break
        tries -= 1
    
    if returnVal == None and essential in kwargs.keys() and kwargs["essential"] == True:
        progTerm(message = "Invalid input provided" + "" if "name" not in kwargs.keys() else "for" + kwargs["name"])
    return returnVal

def progTerm(message="",exitCode = 1, silent = False):
    if not silent:
        print("\tTerminating program with exit code %d.\n\t%s" % exitCode, message)
    sys.exit(exitCode)

