from time import sleep
from bs4 import BeautifulSoup
from httpx import head
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

#import httpx

import re
from numerize import numerize

from news_analysis import NewsAnalyzer

# TODO: inherit from a class called OTCScraper
# Also, make function to return a webdriver to specified url with all the options
class TickerScraper():
    OTCMARKETS_URL = "https://www.otcmarkets.com"
    #whoop = Whoop()
    #whoop_scan_result = whoop.scan()

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.log = ""

    def get_all_text_for(self, url):
        options = Options()
        # options to suppress logging output
        #options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        #options.add_argument("--log-level=3")
        options.add_argument("headless") # run in background
        options.add_argument("--window-size=1920,1080") # prevent mobile emulation

        # emulate user to prevent headless detection
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get(url)
        except:
            self.log += "Driver failed to get {}".format(url)
            return None
        
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        all_text = " ".join(soup.strings)
        return all_text

    def extract_value(self, kind, all_text):
        value = None
        
        # Troubleshooting 404
        self.log += "Checking if {} was found... ".format(TickerScraper.OTCMARKETS_URL)
        if re.search(r"Page Not Found", all_text):
            self.log += "Page Not Found!\n"
            return None
        else:
            self.log += "Page Found.\n"
        
        # parsing
        self.log += "Parsing data for {}...\n".format(kind)
        value_dirty_match = re.search(kind + r"\s*[1-9][0-9]?[0-9]?(,[0-9]{3})*", all_text)
        if value_dirty_match != None:
            value_clean_match = re.search(r"[1-9][0-9]?[0-9]?(,[0-9]{3})*", value_dirty_match.group())
            if value_clean_match != None:
                value_clean = value_clean_match.group()
                value = int(value_clean.replace(',', ''))
                self.log += "Found that {0} has about {1} {2} ({3}).\n".format(
                    self.ticker, numerize.numerize(value), kind.lower(), value_clean)
            else:
                self.log += "Error pulling value of \"{0}\" of {1}\n".format(kind, self.ticker)
        else:
            self.log += "Found no available data for \"{0}\" of {1}\n".format(kind, self.ticker)
        
        return value

    # return as dict
    def extract_security_details(self):
        '''Returns share structure dict'''
        url = "{0}/stock/{1}/security".format(TickerScraper.OTCMARKETS_URL, self.ticker)
        all_text = self.get_all_text_for(url)
        o_s = self.extract_value("Outstanding Shares", all_text) # important so make sure not None, try again...
        if o_s is None:
            sleep(5)
            o_s = self.extract_value("Outstanding Shares", all_text) # trying again
        a_s = self.extract_value("Authorized Shares", all_text)
        r_s = self.extract_value("Restricted", all_text)
        shares = {'Outstanding': o_s, 'Authorized': a_s, 'Restricted': r_s,
            'Unrestricted': o_s - r_s if o_s != None and r_s != None else None,
            'Dilutable': a_s - o_s if a_s != None and o_s != None else None}
        return shares

    def extract_headlines(self): 
        # need to keep clicking more button until "Displaying X of X Press Releases" Use re.findall()
        # to get the relevant numbers. But how to press "More" button...?

        url = "{0}/stock/{1}/news".format(TickerScraper.OTCMARKETS_URL, self.ticker)
        all_text = self.get_all_text_for(url)
        headlines = None
        
        # Troubleshooting 404 - factor this out as another method
        self.log += "Checking if {} was found... ".format(TickerScraper.OTCMARKETS_URL)
        if re.search(r"Page Not Found", all_text):
            self.log += "Page Not Found!\n"
            return None
        else:
            self.log += "Page Found.\n"
        
        # parsing - headline shows up after 8th instance of "News" in page text. Date follows!
        self.log += "Parsing data for latest headline...\n"
        headlines_dirty_match = re.search(r"OTC Disclosure & News Service.*[0-9]{2}/[0-9]{2}/[0-9]{4}", all_text)
        # "(Displaying.*Press Releases|Not available) News.*[0-9]{2}/[0-9]{2}/[0-9]{4}" for just the newswire news

        if headlines_dirty_match != None:
            headlines_clean_match = re.search(r"News.*", headlines_dirty_match.group())
            headlines = headlines_clean_match.group().strip()
            self.log += "Found that {0} has headlines:\n\"{1}.\"\n".format(self.ticker, headlines)
        else:
            self.log += "Found no available headlines for {0}\n".format(self.ticker)
        
        return headlines
    
    # Want to use this in WhoopStock
    def get_analysis_of_news_behavior(self):
        '''
        Returns an analysis of news in a dict. \nKeys:
        'dates' = list of date objects, each representing a day when there was a PR\n
        'freq' = PR frequency (PRs per day)\n
        'ednpr' = Expected Date of Next PR\n
        'edunpr' = Expected Days Until Next PR\n
        'dslpr' = Days Since Last PR\n
        '''
        headlines = self.extract_headlines() # For some reason missing second news section unless done twice.
        headlines = self.extract_headlines() # So, gotta do it again.
        if headlines is None:
            headlines = self.extract_headlines() # Once more for good measure
        news_analyzer = NewsAnalyzer(headlines)
        news_analysis = news_analyzer.analyze()
        return news_analysis

    def __str__(self):
        return "Scraper Summary:\n{}".format(self.log).strip()