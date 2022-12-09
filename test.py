from scrape_otcmarkets import TickerScraper
from news_analysis import NewsAnalyzer
from stock import WhoopStock
import think
from whoop_magus import WhoopMagus
from ddmagic import DDmagic
import re

from whoops import WhoopScan

# Test 1
def test_scrape_otcmarkets():
    print("Test 1: Testing module: scrape_otc_markets / class: TickerScraper")
    ticker = input("Enter ticker symbol: ")
    ticker_scraper = TickerScraper(ticker)
    #security_details  = ticker_scraper.extract_security_details()
    #print(security_details)
    analysis_of_news_behavior = ticker_scraper.get_analysis_of_news_behavior()
    #print(analysis_of_news_behavior)

    dates = analysis_of_news_behavior['dates']
    freq = analysis_of_news_behavior['freq']
    ednpr = analysis_of_news_behavior['ednpr']
    edunpr = analysis_of_news_behavior['edunpr']
    dslpr = analysis_of_news_behavior['dslpr']
    print("\n")
    # Print dates as table with year as row and month/day as column, wrapping to next line after 10 dates
    i = 1
    j = 1
    year = dates[0].year
    print("{}: ".format(year), end="")
    for date in dates:
        if date.year != year:
            year = date.year
            print("\n{}: ".format(year), end="")
            j = 1
        print("" + date.strftime("%m/%d") + "{}".format(", " if j % 10 != 0 and i % len(dates) != 0 else "\n"), end="")
        i += 1
        j += 1
    print()
    print("PRs per day: {0} -> {1} days between PRs.".format(round(freq, 2), round(1/freq, 2)))
    print("PRs per week: {}".format(round(freq * 7, 2)))
    print("PRs per month: {}".format(round(freq * 30, 2)))
    print("Expected date of next PR is {0} days away: {1}".format(edunpr, ednpr.strftime("%m/%d/%Y")))
    print("Days since last PR: {}".format(dslpr))

    #print(ticker_scraper)

# Test 2
def test_stock(): # Add dollar volume to WhoopStock fields!!! # Also add percent float (unrestricted) traded!!!
    # Also add

    print("Test 2: Testing module: stock / class: WhoopStock")
    #opti_scraper = Scraper('opti')
    #opti = WhoopStock('opti', 0.0081, 0.0085, 6505067, 3660000, opti_scraper)
    ticker = input("Enter ticker: ")
    pv = think.get_price_and_volume(ticker)
    prev_cv = think.get_prev_close_and_volume(ticker)
    ticker_scraper = TickerScraper(ticker)
    ticker_stock = WhoopStock(ticker, pv[0],prev_cv[0], pv[1], prev_cv[1], ticker_scraper)
    return ticker_stock

# Test 3
def test_think():
    print("Test 3: Testing module: think")
    ticker = input("Enter ticker: ")
    quote = think.get_quote(ticker)
    candle_yesterday = think.get_candle_yesterday(ticker)
    print("Price for {0}: {1}".format(ticker.upper(), quote['lastPrice']))
    print("Volume for {0}: {1}".format(ticker.upper(), quote['totalVolume']))
    print("Previous close for {0}: {1}".format(ticker.upper(), candle_yesterday['close']))
    print("Previous volume for {0}: {1}".format(ticker.upper(), candle_yesterday['volume']))
    #print(think.get_num_pinks())
    #print(think.get_prev_close_and_volume('DHUA'))
    print("Tested module: think\n")

# Test 4
def test_whoop_magus():
    print("Test 4: Testing module: whoop_magus / class: WhoopMagus")
    scanning_tool = WhoopMagus()
    whoop_stocks = scanning_tool.scan_range(WhoopMagus.available_whoop_dict['Whoop Active'], 2544, 2544)
    print(scanning_tool) # prints whoop summary
    print("Tested module: whoop_magus / class: WhoopMagus\n")

# Test 5
def test_DDmagic():
    print("Test 5: Testing module: ddmagic / class: DDmagic")
    # Make a menu!
    # DDmagic Options: List Whoops, Select Whoop, Change Whoop, Quit

    ddmagic = DDmagic()
    # Whoop options for "Named Whoop": Run scan, Current WhoopStocks, 
                                    # Change whoop, Go Back to DDmagic Main Menu
    #ddmagic.run_scan_range(137, 139)
    ddmagic.run_whoop_magus()
    print(ddmagic)
    # Can select a WhoopStock to view details
    # WhoopStock Options: View Security Details, Cast DDmagic spell
    # DDmagic spell result: iHub DD, Company Twitter feed, Last SEC Filing Type, Date of Last Filing,
                            # Expected Date of Next Filing ("Filing Type")
                            # Date of last PR, last PR title, Average PR Frequency,
                            # Expected Date of Next PR (MAKE THIS FEATURE)
    print("Tested module: ddmagic / class: DDmagic\n")



def run_tests():
    option = input("Enter test number(s): ")
    if re.search(r"1", option):
        test_scrape_otcmarkets()
    if re.search(r"2", option):
        whoop_stock = test_stock()
        print(whoop_stock)
        print("Tested module: stock\n")
    if re.search(r"3", option):
        test_think()
    if re.search(r"4", option):
        test_whoop_magus()
    if re.search(r"5", option):
        test_DDmagic()

run_tests()

#Create class Test Which says Testing (blah blah) / class (or function) blah blah