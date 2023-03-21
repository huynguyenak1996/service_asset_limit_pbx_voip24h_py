import asyncio
from pyami_asterisk import AMIClient

def all_events(events):
    print(events)
async def hangup_call(events):
    """asynchronous callbacks"""
    await asyncio.sleep(1)
    print(events)
ami = AMIClient(host='14.225.251.72', port=7227, username='admin', secret='Voip@Report@092020')
ami.register_event(["*"], all_events)
ami.register_event(["Hangup"], hangup_call)
ami.connect()