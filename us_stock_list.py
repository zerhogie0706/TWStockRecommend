import requests
from itertools import chain
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_TOKEN = os.environ.get('US_STOCK_API_TOKEN')
NYSE_EXCHANGES = 'NYSE'
NASDAQ_EXCHANGES = 'NASDAQ'
EXCHANGES_URL = f'https://eodhd.com/api/exchanges-list/?api_token={API_TOKEN}&fmt=json'
TICKERS_URL = f'https://eodhd.com/api/exchange-symbol-list/%s?api_token={API_TOKEN}&fmt=json'


def get_tickers():
    nyse_data = requests.get(TICKERS_URL % NYSE_EXCHANGES).json()
    NYSE_LIST = (data['Code'] for data in nyse_data)
    nasdaq_data = requests.get(TICKERS_URL % NASDAQ_EXCHANGES).json()
    NASDAQ_LIST = (data['Code'] for data in nasdaq_data)
    return chain(NYSE_LIST, NASDAQ_LIST)

STOCK_IDS = get_tickers()
