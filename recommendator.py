import csv
import os
import yfinance as yf
from datetime import datetime
from functools import reduce
from tw_stock_list import STOCK_IDS as TW_STOCK_IDS
from us_stock_list import STOCK_IDS as US_STOCK_IDS
from utils import suppress_stdout
from constants import *

SYMBOLS = [MACD, VOLUME]


def daily_recommendations(symbols, country='TW'):
    if country not in ALLOWED_COUNTRIES:
        return

    if country == TW:
        STOCK_IDS = TW_STOCK_IDS
    elif country == US:
        STOCK_IDS = US_STOCK_IDS

    # report = {}
    matches = {
        MACD: dict(),
        VOLUME: dict(),
    }
    all_matches_set = set()
    with suppress_stdout():
        for stock_id in STOCK_IDS:
            if country == TW:
                stock_symbol = f'{stock_id}.TW' 
            elif country == US:
                stock_symbol = stock_id
            data = yf.download(stock_symbol, period='3mo')
            if data.empty:
                continue
            # 美股加成交量條件至少1M
            if country == US and list(data['Volume'])[::-1][0] < 1000000:
                continue
            all_matches_count = 0
            for symbol in symbols:
                func = SYMBOL_FUNCTION[symbol]
                if func(data):
                    all_matches_count += 1
                    matches[symbol][stock_id] = list(data['Close'])[::-1][0]

            if all_matches_count == len(SYMBOLS):
                all_matches_set.add(stock_id)

        # report[symbol] = matches
    return matches, all_matches_set


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
    try:
        volume_ratio = list(data['Volume'])[::-1][0] / list(data['VMA5'])[::-1][0]
        return volume_ratio >= 2
    except:
        return False


SYMBOL_FUNCTION = {
    MACD: is_macd_golden_cross,
    VOLUME: is_large_volume,
}


def run(country='TW'):
    matches, all_matches_set = daily_recommendations(SYMBOLS, country)
    today_date = datetime.now().date().strftime('%Y%m%d')
    # intersection = reduce(lambda a, b: a.intersection(b), report.values())
    country_stock = '台股' if country == 'TW' else '美股'
    with open(f"/Users/{os.environ.get('USER')}/Desktop/{today_date}{country_stock}推薦.csv", "a") as file:
        writer = csv.writer(file)
        for symbol, data in matches.items():
            writer.writerow([symbol])
            for ticker, close_prise in data.items():
                writer.writerow([ticker, close_prise])
            # file.writerow([])
        writer.writerow([f'都符合: {all_matches_set}'])
        writer.writerow([])
