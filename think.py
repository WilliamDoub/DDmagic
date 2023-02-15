import atexit
import datetime
import dateutil
import sys
import re

import tda
import httpx
import json

from time import sleep

from scrape_otcmarkets import TickerScraper
from stock import WhoopStock

def make_webdriver():
    from selenium import webdriver
    return webdriver.Chrome(executable_path="/Users/wuhushi/Documents/wcd_Python/chromedriver")


API_KEY = '*********@AMER.OAUTHAP'
URI = 'https://localhost'
TOKEN_PATH = '/Users/wuhushi/Documents/wcd_Python/token.json'
# Making client with above attributes for login flow
c = tda.auth.easy_client(API_KEY, URI, TOKEN_PATH, webdriver_func=make_webdriver)

def get_quote(ticker):
    ticker = ticker.upper()
    try:
        # get last price and total volume from quote
        # add try block
        # r = response
        r = c.get_quote(ticker)
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
    except:
        return None
    
    data = r.json()
    # Handling empty quote dict
    if len(data) == 0:
        return None
    
    quote = data[ticker]
    return quote

def get_price_and_volume(ticker):
        ticker = ticker.upper()
        
        quote = get_quote(ticker)
        # Handling empty quote dict
        if quote is None:
            return None
        
        price = quote['lastPrice']
        volume = quote['totalVolume']
        return [price, volume]

def get_candle_yesterday(ticker):
    ticker = ticker.upper()

    # Handling errors retrieving history
    try:
        # get one month daily history (ohlcv candles)
        # r = response
        r = c.get_price_history(ticker,
            period_type=c.PriceHistory.PeriodType.MONTH,
            period=c.PriceHistory.Period.ONE_MONTH,
            frequency_type=c.PriceHistory.FrequencyType.DAILY,
            frequency=c.PriceHistory.Frequency.DAILY)
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
    except:
        return None
    
    history = r.json()
    # Handling empty history dict
    if len(history) == 0:
        return None
    
    # put daily candles in list
    daily_candles = []
    for candle in history['candles']:
        daily_candles.append(candle)
    if len(daily_candles) > 2:
        return daily_candles[-2]
    else:
        return None

def get_prev_close_and_volume(ticker):
    ticker = ticker.upper()

    candle_yesterday = get_candle_yesterday(ticker)
    # Handling empty history dict
    if candle_yesterday is None:
        return None
    
    prev_close = candle_yesterday['close']
    
    prev_volume = candle_yesterday['volume'] 

    return [prev_close, prev_volume]

def get_pinks():
    '''Returns a list of pink sheet stocks'''
    pinks = []
    # get pink sheet tickers (only 4 letters to avoid massive amount of foreign crap)
    r = c.search_instruments('[A-Z][A-Z][A-Z][A-Z]', c.Instrument.Projection('symbol-regex'))
    all_tickers = r.json()
    for ticker in all_tickers:
        if re.match(r"Pink Sheet", all_tickers[ticker]['exchange']):
            pinks.append(ticker)
    return pinks

def get_num_pinks():
    '''Returns the number of Pink Sheet stocks'''
    pinks = get_pinks()
    return len(pinks)



#json.dumps(history, indent=4)

# Does not work:
# r = c.get_watchlists_for_single_account(account_id='277473774TDA')
