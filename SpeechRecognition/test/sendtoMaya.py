import socket


HOST = '127.0.0.1'
PORT = 54321
ADDR = (HOST, PORT)

def send_command(command='print(\'command socket test\')'):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(command)
    client.close()

def get_command(decoded_command):

    command_dict = {'set timeline to selected': 'set timeline to selected',
                    'timeline to selected': 'set timeline to selected',
                    'set timeline to selection': 'set timeline to selected',
                    'timeline to selection': 'set timeline to selected'}

    matched_command = command_dict[decoded_command]

    if matched_command == 'set timeline to selected':
        description = 'set timeline to selected'
        command = 'import pymel.core as pm\n'
        command += 'try:\n'
        command += '\tprint(\''+description+'\')\n'
        command += '\tfirstframe = min(pm.keyframe(pm.ls(sl=1), q=1))\n'
        command += '\tlastframe = max(pm.keyframe(pm.ls(sl=1), q=1))\n'
        command += '\tpm.playbackOptions(ast=firstframe, aet=lastframe, min=firstframe, max=lastframe)\n'
        command += 'except Exception as e:\n'
        command += '\tprint(e)\n'

    return(command)




decoded_command = get_command('set timeline to selected')
print(decoded_command)
send_command(decoded_command)



send_command()
