'''
The following code is used to access the API of the website ... that offers financial data on cryptocurrency related assets. After reading the documentation, which can be found here ..., the script makes a request to the websever and authenticates (?) using a web-token to obtain access.
'''

import os
import requests
from datetime import datetime
import time
import numpy as numpy
import pandas as pd

'''
Coingecko API is being used to collect information of the most recent developments and price activity from the cryptocurrency financial markets. 
The Coingecko API was chosen because it offers a wide range of assets and offer free API access up to limit of 10-30 calls/minute, and doesn't come with API key.
Initially a permission request was made by e-mail if it was possible to scrape their front-page once a day for educational purposes this however was rejected.
The API provides us with same information while following legal policies provided by CoinGecko and combined with their documentation help us explore a different way to
obtain data from the web.

For more information regarding CoinGecko's API, information can be found in their official documentation:
https://www.coingecko.com/en/api/documentation
'''

currency = 'bitcoin'
data = 'ohlc'
api_url = f'https://api.coingecko.com/api/v3/coins/{currency}/{data}?vs_currency=usd&days=1&precision=2' #Get the latest 24H OHLC data for bitcoin versus usd, precision rounded to 2 decimals.

# Python file location
script_dir = os.path.dirname(__file__)

out_file_name = f'api_coingecko_{currency}_{data}_{datetime.utcnow().isoformat()}.csv'

state = {
    'start_dt': datetime.utcnow(),
    'response_dt': '',
    'error': '',
    'status_code': '',
    'success': False,
    'data': {},
}

#################################################
### Custom functions
# Parse messages to log in enriched format which includes the isotime, function
def log(func_name='', state='', update='', message='')->None:
    utc_now = datetime.utcnow()
    print(f'\n\033[1m{utc_now.isoformat()} <{func_name}> [{state}][{update}]:\033[0m\n{message}')

#################################################
### Everything below here is logic for api
### API will send the following data   timestamp, open, high, low, close
def get_api(src)->None:
    try:
        res = requests.get(src)
        
        if(res.status_code == 200):
            res_json = res.json()

            #Set state values
            state['response_dt'] = datetime.utcnow()
            state['status_code'] = 200
            state['success'] = True
            state['data'] = res_json

            #Print logging out to console
            log('get_api','OK',res.status_code,res_json)

            #Convert api data to a pandas dataframe and export as csv
            write_data = os.path.join(script_dir, './data/data_')
            df_api = get_dataframe_api(state)
            df_api.to_csv(write_data+out_file_name, index=False)

            #Save the state to the logs and export to csv
            write_log = os.path.join(script_dir, './logs/log_')
            df_log = get_dataframe_log(state)
            df_log.to_csv(write_log+out_file_name,index=False)

        else:
            #Set state values
            state['response_dt'] = datetime.utcnow()
            state['status_code'] = res.status_code
            state['success'] = False
            state['error'] = res.reason

            #Print logging out to console
            log('get_api','FAIL',res.status_code,res.reason)

            print(state)

            #Save the state to the logs and export as csv
            write_log = os.path.join(script_dir, './logs/log_')
            df_log2 = get_dataframe_log(state)
            df_log2.to_csv(write_log+out_file_name,index=False)
            
    except Exception as e:
        #Set state values
        state['response_dt'] = datetime.utcnow()
        state['status_code'] = res.status_code
        state['success'] = False
        state['error'] = e

        #Print logging out to console
        log('get_api','ERROR',res.status_code,res.reason)

        #Save the state to the logs
        df_log3 = get_dataframe_log(state)
        write_log = os.path.join(script_dir, './logs/log_')
        df_log3.to_csv(write_log+out_file_name,index=False)

def get_dataframe_api(state)->pd.DataFrame():
    df = pd.DataFrame(
        data=state['data'],
        columns=['timestamp','open','high','low','close']
        )
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def get_dataframe_log(state)->pd.DataFrame():
    data = pd.Series(state).to_frame().T
    df = pd.DataFrame(data=data,columns=state.keys())
    df['start_dt'] = pd.to_datetime(df['start_dt'])
    df['response_dt'] = pd.to_datetime(df['response_dt'])
    df.drop(columns=['data'],inplace=True)
    return df
    
get_api(api_url)




