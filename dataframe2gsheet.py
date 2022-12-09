from time import sleep
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scrape_otcmarkets import TickerScraper
from stock import WhoopStock
import think
from whoop_magus import WhoopMagus
from whoops import Whoop
from numerize import numerize
from datetime import date
import spreadsheet_config as s_config
from worksheet_util import *

whoop_magus = WhoopMagus()
whoop_stocks = whoop_magus.scan(WhoopMagus.available_whoop_dict['Whoop Scan'])
#whoop_stocks = whoop_magus.scan_range(WhoopMagus.available_whoop_dict['Whoop Active'], 2535, 2544)


historical_data = {
    'Date': date.today().strftime("%m/%d"),
    'Ticker': [w.ticker for w in whoop_stocks],
    'Market Cap': [w.market_cap for w in whoop_stocks],
    'Price': [w.price for w in whoop_stocks],
    'Price % Change': [w.price_percent_change / 100 for w in whoop_stocks],
    'Previous Close': [w.prev_close for w in whoop_stocks],
    'Price Net Change': [w.price_net_change for w in whoop_stocks],
    '(Ticker)': [w.ticker for w in whoop_stocks],
    '$ Volume': [w.dollar_volume for w in whoop_stocks],
    'Volume': [w.volume for w in whoop_stocks],
    'Volume % Change': [w.volume_percent_change / 100 for w in whoop_stocks],
    'Previous Volume': [w.prev_volume for w in whoop_stocks],
    'Volume Net Change': [w.volume_net_change for w in whoop_stocks],
    '[Ticker]': [w.ticker for w in whoop_stocks],
    'Outstanding': [w.shares['Outstanding'] for w in whoop_stocks],
    'Authorized': [w.shares['Authorized'] for w in whoop_stocks],
    'Dilutable': [w.shares['Dilutable'] for w in whoop_stocks],
    'Unrestricted': [w.shares['Unrestricted'] for w in whoop_stocks],
    'Restricted': [w.shares['Restricted'] for w in whoop_stocks],
    '% Float Traded': [w.percent_float_traded / 100 if w.percent_float_traded is not None else None for w in whoop_stocks]
}

df_historical = pd.DataFrame(data=historical_data)

insert_at_next_row_in_sheet(s_config.service_file_path, s_config.spreadsheet_id, s_config.sheet_name2, df_historical)


#data = {'col1': [1, 2], 'col2': [3, 4]}
data = {
    'Ticker': historical_data['Ticker'],
    'Market Cap': historical_data['Market Cap'],
    'Price': historical_data['Price'],
    'Price % Change': historical_data['Price % Change'],
    'Previous Close': historical_data['Previous Close'],
    'Price Net Change': historical_data['Price Net Change'],
    '(Ticker)': historical_data['Ticker'],
    '$ Volume': historical_data['$ Volume'],
    'Volume': historical_data['Volume'],
    'Volume % Change': historical_data['Volume % Change'],
    'Previous Volume': historical_data['Previous Volume'],
    'Volume Net Change': historical_data['Volume Net Change'],
    '[Ticker]': historical_data['Ticker'],
    'Outstanding': historical_data['Outstanding'],
    'Authorized': historical_data['Authorized'],
    'Dilutable': historical_data['Dilutable'],
    'Unrestricted': historical_data['Unrestricted'],
    'Restricted': historical_data['Restricted'],
    '% Float Traded': historical_data['% Float Traded']
}

'''
# adding news analysis - is not working
for w in whoop_stocks:
    sleep(5)
    news_analysis = w.analyze_my_news_history()
    data['Avg Weekly PRs'] = news_analysis['freq'] * 7 if news_analysis['freq'] is not None else None
    data['Exp. Days Until PR'] = news_analysis['edunpr']
    data['Exp. PR date'] = news_analysis['ednpr'].strftime("%m/%d/%Y") if news_analysis['ednpr'] is not None else None
    data['Avg Days b/w PR'] = 1 / news_analysis['freq'] if news_analysis['freq'] is not None else None
    data['Days Since Last PR'] = news_analysis['dslpr']
'''

df = pd.DataFrame(data=data)

data_pretty = data
data_pretty['Market Cap'] = list(map(WhoopStock.smart_numerize, data_pretty['Market Cap']))
data_pretty['Volume'] = list(map(WhoopStock.smart_numerize, data_pretty['Volume']))
data_pretty['Previous Volume'] = list(map(WhoopStock.smart_numerize, data_pretty['Previous Volume']))
data_pretty['Volume Net Change'] = list(map(WhoopStock.smart_numerize, data_pretty['Volume Net Change']))
data_pretty['Price % Change'] = list(map(lambda x: round(x, 2), data_pretty['Price % Change']))
data_pretty['Volume % Change'] = list(map(lambda x: round(x, 2), data_pretty['Volume % Change']))

data_pretty = data
data_pretty['ticker'] = None
df_pretty = pd.DataFrame(data=data_pretty, index=[w.ticker for w in whoop_stocks])

'''
print(df)
print()
print(df_pretty)

df.plot.bar()
plt.show(block=True)
'''

overwrite_to_gsheet(s_config.service_file_path, s_config.spreadsheet_id, s_config.sheet_name1, df)
