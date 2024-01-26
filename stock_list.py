import twstock
import pandas as pd
import requests


STOCK_IDS2 = (code for code in twstock.twse.keys())

def get_stock_ids():
    res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    df = pd.read_html(res.text)[0]
    filtered_df = df[df[0].apply(lambda x: len(x.split('\u3000')[0]) == 4)]
    stock_columns = list(filtered_df[0])
    stock_ids = [data.split('\u3000')[0] for data in stock_columns]
    return stock_ids

STOCK_IDS = get_stock_ids()
