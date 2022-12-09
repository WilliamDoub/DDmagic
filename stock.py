from numerize import numerize
from scrape_otcmarkets import TickerScraper

class WhoopStock():
    def __init__(self, ticker, price, prev_close, volume, prev_volume, ticker_scraper: TickerScraper):
        # might want to pass ticker_scraper object instead (to easily add more data, less params)
        self.ticker = ticker.upper()
        self.price = price
        self.prev_close = prev_close
        self.price_net_change = price - prev_close if price is not None and prev_close is not None else None
        if self.prev_close is not None and self.prev_close > 0:
            self.price_percent_change = self.price_net_change / prev_close * 100
        else:
            self.price_percent_change = None
        
        self.volume = volume
        self.prev_volume = prev_volume
        self.volume_net_change = volume - prev_volume if volume is not None and prev_volume is not None else None
        if prev_volume is not None and prev_volume > 0:
            self.volume_percent_change = self.volume_net_change / prev_volume * 100
        else:
            self.volume_percent_change = None

        if prev_close is not None and price is not None and volume is not None:
            self.dollar_volume = (price + prev_close) / 2 * volume  # ~avg dollar volume (today) for stock that went up
        else:
            self.dollar_volume = None

        self.shares = ticker_scraper.extract_security_details()
        o_s = self.shares['Outstanding']
        self.market_cap = o_s * price if o_s is not None and price is not None else None
        unrestricted = self.shares['Unrestricted']
        self.percent_float_traded = volume / unrestricted * 100 if unrestricted is not None and volume is not None else None

    def analyze_my_news_history(self):
        '''
        Returns an analysis of my news in a dict (by making and using a TickerScraper). \nKeys:
        'dates' = list of date objects, each representing a day when there was a PR\n
        'freq' = PR frequency (PRs per day)\n
        'ednpr' = Expected Date of Next PR\n
        'edunpr' = Expected Days Until Next PR\n
        'dslpr' = Days Since Last PR\n
        '''
        ticker_scraper = TickerScraper(self.ticker)
        return ticker_scraper.get_analysis_of_news_behavior()
    
    @staticmethod
    def pretty_change(ugly_change, numerize_on: bool):
        if ugly_change is None:
            return None
        result = ""
        if ugly_change >= 0:
            result += "+"
        
        if numerize_on:
            result += numerize.numerize(ugly_change)
        else:
            result += str(round(ugly_change, 4))
        
        return result
    
    @staticmethod
    def smart_numerize(value):
        return numerize.numerize(value) if value is not None else None

    # CONSIDER making stored variables, vs pretty display variables -> organization


    def __str__(self):
        summary = "Whoop Data for {0}:\nPrice: {1} = {2}% ".format(
            self.ticker, self.price, WhoopStock.pretty_change(self.price_percent_change, True))
        summary += "of {0} (a net change of {1})\n".format(self.prev_close, 
            WhoopStock.pretty_change(self.price_net_change, False))
        summary += "Volume: {0} = {1}% ".format(
            numerize.numerize(self.volume), WhoopStock.pretty_change(self.volume_percent_change, True))
        summary += "of {0} (a net change of {1})\n".format(WhoopStock.smart_numerize(self.prev_volume), 
            WhoopStock.pretty_change(self.volume_net_change, True))
        summary += "Market Cap: {}\n".format(WhoopStock.smart_numerize(self.market_cap))
        summary += "Share Structure: \n"
        i = 0
        for kind in self.shares:
            amount = self.shares[kind] if self.shares[kind] != None else None
            summary += "{}: ".format(kind)
            if i == 0:
                summary += " "
            elif i == 1 or i == 2:
                summary += "  "
            elif i == 4:
                summary += "   "
            
            if self.shares[kind] != None:
                summary += "{0} ({1:,})\n".format(numerize.numerize(amount), amount)
            else:
                summary += "{0}\n".format(amount)
            i += 1

        return summary
