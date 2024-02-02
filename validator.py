import csv
import yfinance as yf
import pandas as pd

STOCK_TICKET_LIST = []

def validate(stock_ticker_list, country='TW'):
    result = []
    for stock_ticker in stock_ticker_list:
        if country == 'TW':
            stock_ticker = f'{stock_ticker}.TW'
        try:
            data = yf.download(stock_ticker, period='5d')
            close = [round(value, 2) for value in list(data['Close'])[::-1][:2]]
        except:
            close = [0, 0]
        result.append(close)

    with open('validateTW-0128.csv', 'w') as file:
        writer = csv.writer(file)
        for close in result:
            writer.writerow(close)


def get_data_from_csv(file_name):
    df = pd.read_csv(file_name)
    return list(df['MACD'])[:-1]


def test():
    file_name = 'USStockRecommendation20240128.csv'
    ticker_list = get_data_from_csv(file_name)
    validate(ticker_list)
