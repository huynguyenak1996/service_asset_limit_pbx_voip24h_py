from asterisk.ami import *

client = AMIClient(address='14.225.251.72',port=5038)
client.login(username='root',secret='PBXVoip24h@dmin')

action = SimpleAction(
    'Originate',
    Channel='SIP/901',
    Exten='902',
    Priority=1,
    Context='dev',
    CallerID='python',
)
client.send_action(action)
print(client)