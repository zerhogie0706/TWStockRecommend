import yfinance as yf
from datetime import datetime
from functools import reduce
from stock_list import STOCK_IDS
from utils import suppress_stdout

SYMBOLS = ['MACD', 'VOLUMNE']


def daily_recommendations(symbols):
    report = {}
    for symbol in symbols:
        func = SYMBOL_FUNCTION[symbol]
        matches = set()
        # IS_GOLDEN_CROSS = set()
        with suppress_stdout():
            for stock_id in STOCK_IDS:
                stock_symbol = f'{stock_id}.TW'
                data = yf.download(stock_symbol, period='3mo')
                if func(data):
                    matches.add(stock_id)
        report[symbol] = matches
    return report


def is_macd_golden_cross(data):
    try:
        data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
        data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = data['EMA12'] - data['EMA26']
        data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['Bar'] = data['MACD'] - data['Signal']
        return list(data['Bar'])[::-1][0] > 0 and list(data['Bar'])[::-1][1] < 0 and list(data['MACD'])[::-1][0] > 0
    except:
        return False


def is_large_volume(data):
    data['VMA5'] = data['Volume'].ewm(span=5, adjust=False).mean()
    volume_ratio = list(data['Volume'])[::-1][0] / list(data['VMA5'])[::-1][0]
    return volume_ratio >= 2


SYMBOL_FUNCTION = {
    'MACD': is_macd_golden_cross,
    'VOLUMNE': is_large_volume,
}


report = daily_recommendations(SYMBOLS)
today_date = datetime.now().date().strftime('%Y%m%d')
intersection = reduce(lambda a, b: a.intersection(b), report.values())
with open(f'/Users/chia-weihsu/Desktop/台股推薦.txt', 'a') as file:
    for symbol, matches in report.items():
        file.write(f'{today_date} {symbol}: {matches}\n')
        file.write('-' * 20 + '\n')
    file.write(f'都符合: {intersection}\n')
    file.write('-' * 20 + '\n')
