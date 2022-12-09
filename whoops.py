from scrape_otcmarkets import TickerScraper
from stock import WhoopStock
import think
# For some reason if running Generic Whoop after Quoteable Whoop, 5th returned WhoopStock lacks share data
class Whoop():
    '''Generic Whoop. If used to scan, will actually return all sampled tickers as WhoopStocks'''
    def __init__(self):
        self.whoop_stocks: list[WhoopStock] = []
        self.name = "Whoop Generic"
    
    def analyze(self, ticker):
        '''Generic analyze gathers info and returns true for any stock'''
        # Get price and volume
        pv = think.get_price_and_volume(ticker)
        if pv is None:
            price = None
            volume = None
        else:
            price = pv[0]
            volume = pv[1]

        # Get previous close and volume
        prev_cv = think.get_prev_close_and_volume(ticker)
        if prev_cv is None:
            prev_close = None
            prev_volume = None
        else:
            prev_close = prev_cv[0]
            prev_volume = prev_cv[1]
        
        # Get security details
        ticker_scraper = TickerScraper(ticker)
        whoop_stock = WhoopStock(
            ticker, price, prev_close, volume, prev_volume, ticker_scraper)
        for w in self.whoop_stocks:
            if w.ticker == ticker:
                self.whoop_stocks.remove(w)
        self.whoop_stocks.append(whoop_stock)
        return True

    def get_num_whoop_stocks(self):
        return len(self.whoop_stocks)
    
    def __str__(self):
        summary = "\"{}\" found ".format(self.name)
        # Return WhoopStock strings
        n = self.get_num_whoop_stocks()
        plurality = "s"
        plurality_2 = "them"
        if n == 1:
            plurality = ""
            plurality_2 = "it"

        summary += "{0} WhoopStock{1}:\n".format(n, plurality)
        
        for w in self.whoop_stocks:
            summary += str(w) + "\n"
        
        summary += "Done displaying data for {0} WhoopStock{1} from \"{2}\". ".format(n, plurality, self.name)
        summary += "Hope you enjoy {}.\n".format(plurality_2)
        return summary

class WhoopQuotable(Whoop):
    '''Like Generic Whoop but only includes tickers with available quote'''
    def __init__(self):
        super().__init__()
        self.name = "Whoop Quotable"

    def analyze(self, ticker):
        # Get price and volume
        pv = think.get_price_and_volume(ticker)
        if pv is None:
            return False
        else:
            price = pv[0]
            volume = pv[1]
        
        # Get previous close and volume
        prev_cv = think.get_prev_close_and_volume(ticker)
        if prev_cv is None:
            prev_close = None
            prev_volume = None
        else:
            prev_close = prev_cv[0]
            prev_volume = prev_cv[1]
        
        # Get security details
        ticker_scraper = TickerScraper(ticker)
        whoop_stock = WhoopStock(
            ticker, price, prev_close, volume, prev_volume, ticker_scraper)
        for w in self.whoop_stocks:
            if w.ticker == ticker:
                self.whoop_stocks.remove(w)
        self.whoop_stocks.append(whoop_stock)
        return True

class WhoopActive(Whoop):
    '''Like Quotable Whoop, but volume must be greater than 0'''
    def __init__(self):
        super().__init__()
        self.name = "Whoop Active"
    
    def analyze(self, ticker):
        # Get price and volume
        pv = think.get_price_and_volume(ticker)
        if pv is None:
            return False
        else:
            price = pv[0]
            volume = pv[1]
        
        # Get previous close and volume
        prev_cv = think.get_prev_close_and_volume(ticker)
        if prev_cv is None:
            prev_close = None
            prev_volume = None
        else:
            prev_close = prev_cv[0]
            prev_volume = prev_cv[1]

        # Want there to be activity, i.e. volume > 0
        if volume <= 0:
            return False
        
        # Get security details
        ticker_scraper = TickerScraper(ticker)
        whoop_stock = WhoopStock(
            ticker, price, prev_close, volume, prev_volume, ticker_scraper)
        for w in self.whoop_stocks:
            if w.ticker == ticker:
                self.whoop_stocks.remove(w)
        self.whoop_stocks.append(whoop_stock)
        return True


# Each whoop has an analysis function (to anlyze if one ticker meets criteria)
class WhoopScan(Whoop):
    '''
    Contains method to analyze whether a ticker has momentum.
    Uses: Price, Volume, Previous Price, Previous Volume
    Price: < $1
    Price Percent Change: >= 0%
    Volume: >= 50M
    Volume Percent Change: >= 10%
    '''
    def __init__(self):
        super().__init__()
        self.name = "Whoop Scan"

    def analyze(self, ticker: str):
        '''
        Analyzes if a ticker meets criteria:
        Price: < $1
        Price Percent Change: >= 0%
        Volume: >= 50M
        Volume Percent Change: >= 10%
        '''
        # ANALYZE
        # Get price and volume
        # NOTE - could get scrape delayed price and volume from otcmarkets.com to halve time
        pv = think.get_price_and_volume(ticker)
        if pv is None:
            return False
        price = pv[0]
        volume = pv[1]
        # Check price and volume absolute criteria
        if price < 1 and volume > 50000000:
            # Get previous close and volume
            prev_cv = think.get_prev_close_and_volume(ticker)
            if prev_cv is None:
                return False
            prev_close = prev_cv[0]
            prev_volume = prev_cv[1]
            # Check price and volume relative criteria
            if price - prev_close >= 0 and prev_volume > 0 and volume >= prev_volume * 1.10:
                ticker_scraper = TickerScraper(ticker)
                whoop_stock = WhoopStock(
                    ticker, price, prev_close, volume, prev_volume, ticker_scraper)
                for w in self.whoop_stocks:
                    if w.ticker == ticker:
                        self.whoop_stocks.remove(w)
                self.whoop_stocks.append(whoop_stock)
                return True
            else:
                return False
        else:
            return False

# class WhoopMarketCap
# class WhoopSoonPR
# class WhoopSoonHighFreqPR
# class WhoopCaren
