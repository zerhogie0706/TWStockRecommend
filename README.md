# TWStockRecommend

- 以 MACD黃金交叉 / 成交量爆大量 條件篩選台股

- 先修正stock.sh /Users/{user}/Desktop/TWStockRecommend/recommendator.py

- 測試: sh stock.sh

- 排程: crontab -e => 0 18 * * 1-5 /Users/{user}/Desktop/TWStockRecommed/stock.sh  #每週1-5 18點執行

- python3 -m venv venv

- source venv/bin/activate

- pip3 install -r requirements.txt 
