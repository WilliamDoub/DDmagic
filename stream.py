import atexit
import datetime
import dateutil
import sys
import re

from time import sleep

import tda
from tda.streaming import StreamClient
import httpx
import json
import asyncio

def make_webdriver():
    from selenium import webdriver
    return webdriver.Chrome(executable_path="/Users/wuhushi/Documents/wcd_Python/chromedriver")


API_KEY = 'ADKJNQJAJZSQMS1CGEO5MTTCT0KJRYHB@AMER.OAUTHAP'
URI = 'https://localhost'
TOKEN_PATH = '/Users/wuhushi/Documents/wcd_Python/token.json'
# Making client with above attributes for login flow
c = tda.auth.easy_client(API_KEY, URI, TOKEN_PATH, webdriver_func=make_webdriver)

# Stream Data
stream_client = StreamClient(c, account_id='277473774TDA')

stream_client.login()

async def read_stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)

    def print_message(message):
      print(json.dumps(message, indent=4))

    # Always add handlers before subscribing because many streams start sending
    # data immediately after success, and messages with no handlers are dropped.
    stream_client.add_nasdaq_book_handler(print_message)
    await stream_client.nasdaq_book_subs(['GOOG'])

    while True:
        await stream_client.handle_message()

asyncio.run(read_stream())