import json
import globals
def action(data):
    data = json.loads(data)
    if data['e'] == "name":
        if data['dir'] == "get":
            return json.dumps({'e':'name','dir':'post','d':globals.user})
        elif data['dir'] == "post":
            print("connected with {}".format(data['d']))
            globals.state['connectedTo'] = data['d']
    elif data['e'] == "key":
        if data['dir'] == "get":
            pass
        elif data['dir'] == "post":
            pass
    elif data['e'] == "msg":
        print("[{}]: {}" % globals.state['connectedTo'],data['d'])
    return json.dumps({'e':'idle'})

def sendMsg():
    try:
        message = input(globals.user+": ")
        dataSerialise = json.dumps({
            'e':'msg',
            'd':message
            })
        return dataSerialise
    except:
        return
