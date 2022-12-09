import tda
from time import sleep

from scrape_otcmarkets import TickerScraper
import think
from whoops import Whoop, WhoopActive, WhoopQuotable, WhoopScan

class WhoopMagus():
    pinks = think.get_pinks()
    whoop_scan = WhoopScan()
    whoop = Whoop()
    whoop_quotable = WhoopQuotable()
    whoop_active = WhoopActive()
    available_whoop_list = [whoop_scan, whoop, whoop_quotable, whoop_active]
    available_whoop_dict = {'Whoop Scan': whoop_scan, 
                            'Whoop Generic': whoop, 
                            'Whoop Quotable': whoop_quotable, 
                            'Whoop Active': whoop_active}
    num_available_whoops = len(available_whoop_list)

    '''Runs whoop scans'''
    def __init__(self):
        self.log = ""
        self.used_whoops = []
    
    def scan(self, whoop: Whoop):
        self.used_whoops.append(whoop)
        # SCAN and output
        i = 1
        for ticker in self.pinks:
            print("{0}: {1} ".format(i, ticker), end="")
            # Analyze if ticker falls under Whoop criteria, and update loop index
            analysis = whoop.analyze(ticker)
            if (analysis):
                print("is a WhoopStock!", end="")
            print()
            sleep(1)
            i += 1
        
        return whoop.whoop_stocks
    
    #Should really make this an option of regular scan method
    def scan_range(self, whoop: Whoop, start: int, end: int):
        self.used_whoops.append(whoop)
        # SCAN
        i = 1
        for ticker in WhoopMagus.pinks:
            
            # limiting range
            if i < start:
                i += 1
                continue
            elif i > end:
                print()
                break
            else:
                print("{0}: {1} ".format(i, ticker), end="")
            # Analyze if ticker under Whoop criteria, and update loop index
            analysis = whoop.analyze(ticker)
            if (analysis):
                print("is a WhoopStock!", end="")
            print()
            sleep(1)
            i += 1
        
        return whoop.whoop_stocks
    
    def pretty_whoop_names_list(self, whoop_list: list[Whoop]):
        result = ""
        n = len(whoop_list)
        i = 1
        for whoop in whoop_list:
            result += "\"{0}\"{1}".format(whoop.name, ", " if i < n else "")
            i += 1
        return result

    def get_num_used_whoops(self):
        return len(self.used_whoops)
    
    def _get_log(self):
        return "WhoopMagus Logs: \n" + self.log # not yet implemented
    
    def __str__(self):
        summary = "WhoopMagus Summary:\n"
        summary += "Provided Whoops: " + self.pretty_whoop_names_list(self.used_whoops) + "\n"
        
        for whoop in self.used_whoops:
            summary += str(whoop) + "\n"
        
        return summary
