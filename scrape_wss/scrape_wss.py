''' 
https://www.bitmex.com/app/wsAPI
BitMEX offers a complete pub/sub API with table diffing over WebSocket. You may subscribe to real-time changes on any available table.

https://pypi.org/project/websocket-client/
pip install websocket-client
''' 

from datetime import datetime
import websocket
import _thread
import threading
import atexit
import sys
import time
import json
import os

# Python file location
script_dir = os.path.dirname(__file__)

# Flag to indicate if the program should terminate
terminate_flag = False

wss_url = 'wss://ws.bitmex.com/realtime'
op = 'subscribe'
trade = 'XBTUSD'
subscribe = "{"+f'"op": "{op}", "args": ["trade:{trade}"]'+"}"
terminate_timeout = 4 * 60 * 60 # 4 hours * 60 minutes * 60 seconds

state = {
    'last_update':datetime.utcnow(),
    'init':True,
    'num_updates':0,
    'num_errors':0,
    'total_pong':0,
    'total_timeout':0,
    'total_reconnect':0,
    'file_name':f'wss_bitmex_{op}_trade:{trade}_{datetime.utcnow().isoformat()}.csv',
    'init_log':False,
    'init_data':False
}

# Bitmex Recommendation from their official API documentation
# Heartbeats
# Some WebSocket libraries are better than others at detecting connection drops. If your websocket library supports hybi-13, or ping/pong, you may send a ping at any time and the server will return with a pong.
# Due to changes in browser power-saving modes, we no longer support expectant pings via the WebSocket API.
# If you are concerned about your connection silently dropping, we recommend implementing the following flow:
#     After receiving each message, set a timer a duration of 5 seconds.
#     If any message is received before that timer fires, restart the timer.
#     When the timer fires (no messages received in 5 seconds), send a raw ping frame (if supported) or the literal string 'ping'.
#     Expect a raw pong frame or the literal string 'pong' in response. If this is not received within 5 seconds, throw an error or reconnect.

#################################################
### Custom functions
# Parse messages to log in enriched format which includes the isotime, function
def log(func_name='', state='', update='', message=''):
    utc_now = datetime.utcnow()
    print(f'\n\033[1m{utc_now.isoformat()} <{func_name}> [{state}][{update}]:\033[0m\n{message}')

    #Call write_log which saves these as entries in csv log file.
    write_log(func_name,state,update,message)

def write_file(data):
    #New filename for current session
    file_name = 'data_'+state['file_name']
    write_data = os.path.join(script_dir, './data/') + file_name

    if(not state['init_data']):
        with open(write_data,mode='w') as file:
            types = {
                'timestamp': 'timestamp', 
                'symbol': 'symbol', 
                'side': 'symbol', 
                'size': 'long', 
                'price': 'float', 
                'tickDirection': 'symbol', 
                'trdMatchID': 'guid', 
                'grossValue': 'long', 
                'homeNotional': 'float', 
                'foreignNotional': 'float', 
                'trdType': 'symbol'
                }
            keys = list(types.keys())
            colums = ','.join(keys)
            file.write(colums)
            print('Created data file with columns:',colums)
        state['init_data'] = True
    
    #CSV header has been written and file exists
    if(state['init_data']):
        with open(write_data,mode='a') as file:
            for trade in data:
                values = list(trade.values())
                row = '\n' + ','.join(map(str, values)) 
                file.write(row)
                print('\nAppended to data file:',row)

def write_log(_func_name='', _state='', _update='', _message=''):
    #New filename for current session
    file_name = 'log_'+state['file_name']
    write_logs = os.path.join(script_dir, './logs/') + file_name

    if(not state['init_log']):
        with open(write_logs,mode='w') as file:
            file.write('timestamp, last_update, init, num_updates, num_errors, total_pong, total_timeout, total_reconnect, func_name, state, update, message')
            print('Created log file!')
        state['init_log'] = True
    
    #CSV header has been written and file exists
    if(state['init_log']):
        #If it exists, add new entries using append
        print('Appended to log file!')
        with open(write_logs,mode='a') as file:
            timestamp = datetime.utcnow().isoformat()
            # timestamp, last_update, init, num_updates, num_errors, total_pong, total_timeout, total_reconnect, func_name, state, update, message

            #Remove inserting ACTION messages to declutter logs, set to empty 
            if(_state == 'ACTION'):
                _message = ''
            file.write(
                    '\n'
                    + str(timestamp) + ',' + str(state['last_update']) + ',' + str(state['init']) + ',' + str(state['num_updates']) + ',' + str(state['num_errors']) + ',' 
                    + str(state['total_pong']) + ',' + str(state['total_timeout']) + ',' + str(state['total_reconnect']) + ','
                    + str(_func_name) + ',' + str(_state) + ',' + str(_update) + ', "' + str(_message).replace('"',"'") + '"'
            )

#################################################
### Everything below here is logic for websocket

def on_message(ws, message):
    # message contains json in string format, parse string using json.loads()
    # The websocket start with welcome message:
    # {'info': 'Welcome to the BitMEX Realtime API.', 'version': '2.0.0', 'timestamp': '2023-07-13T03:17:33.404Z', 'docs': 'https://www.bitmex.com/app/wsAPI', 'heartbeatEnabled': False, 'limit': {'remaining': 179}}
    # After subscribing a confirmation message is returned:
    # {'success': True, 'subscribe': 'trade', 'request': {'op': 'subscribe', 'args': ['trade']}
    # Subsequent updates are received from the channels that have been subscribed to, 
    # first the channel sends a 'action':'partial' which is a snapshot of most recent state
    # Partial update has following keys: dict_keys(['table', 'action', 'keys', 'types', 'filter', 'data'])
    # All following updates have keys: dict_keys(['table', 'action', 'data'])

    last_update = datetime.utcnow()

    #In case the wss did not return a json object, catch the error with try/except block for further analysis.
    try:
        
        #Turn string into json object
        md = json.loads(message)

        #For the keys, check what is available. This shows what the type of message is.
        if('info' in md.keys()):
            #Info message
            log('on_message','INFO',update='limit',message=md['limit'])

        elif('subscribe' in md.keys()):
            #Subscribe message
            print('SUBSCRIBE',md)
            log('on_message','SUBSCRIBE',update=md['success'],message=md['subscribe'])

        elif('action' in md.keys()):
            #Update tracker
            state['num_updates'] += 1

            #action: partial or insert 
            if(md['action'] == 'partial'):
                log('on_message','ACTION','partial',message=md)
                write_file(md['data'])

            elif(md['action'] == 'insert'):
                log('on_message','ACTION','insert',message=md)
                write_file(md['data'])

        else:
            log('on_message','OTHER','',message=md)

    except Exception as e:
        state['num_errors'] += 1
        log('on_message','ERROR',message=e)

def on_pong(ws, message):
    last_update = datetime.utcnow()
    log('on_pong','HEARTBEAT','response',message='pong')

def on_error(ws, error):
    last_update = datetime.utcnow()
    # Potential errors
    # 2023-07-13T04:31:26.714720 <on_error> [ERROR][Connection to remote host was lost.]:
    # Followed by websocket automatically reopening connection
    # This includes a new partial snapshot followed by insert updates
    # We should compare if the old state already contains the data in the new partial or that we have to add more recent entries and insertions.
    state['num_errors'] += 1
    log('on_error','ERROR',error)

def on_close(ws, close_status_code, close_msg):
    last_update = datetime.utcnow()
    log('on_close','CLOSE',update=close_status_code,message=close_msg)

def on_open(ws):
    state['last_update'] = datetime.utcnow()
    
    if(not state['init']):
        state['total_reconnect'] += 1

    log('on_open','OPEN','ok',message="Connection opened on websocket!")
    log('on_open','SUBSCRIBE','send',message=subscribe)

    #Set init variable to False, to check for consequent restarts
    state['init'] = False
    ws.send(subscribe)

# Terminate websocket gracefully
def close_websocket_on_exit(ws):
    ws.close()
    print("WebSocket connection closed on program exit.")

def terminate_program():
    global terminate_flag
    print("Terminating the program after specified duration.")
    terminate_flag = True
    sys.exit(0)

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wss_url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close,
                              on_pong=on_pong
                              )

    # Register the close_websocket_on_exit function to be called on program exit
    atexit.register(close_websocket_on_exit, ws)

    # Start the WebSocket thread
    _thread.start_new_thread(ws.run_forever, (), {'ping_interval': 10, 'ping_timeout': 5, 'reconnect': 5})

    # Schedule program termination after 4 hours (4 hours * 60 minutes * 60 seconds)
    threading.Timer(terminate_timeout, terminate_program).start()

    try:
        while not terminate_flag:
            # Keep the main thread running, you can add other tasks here if needed
            pass
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Closing WebSocket...")
        ws.close()
        terminate_flag = True
        sys.exit(0)  # Terminate the program gracefully
