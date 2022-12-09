import re
from datetime import datetime, timedelta, date

class NewsAnalyzer():
    def __init__(self, headlines):
        self.headlines = headlines
        self.analysis = {}
        self.log = ""

    def get_dates_from_headlines(self, headlines):
        if headlines is None:
            return None
        dates = []
        dates_match = re.findall(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", headlines)
        if dates_match != None:
            dates_string_dup_check = []
            for date in dates_match:
                if date not in dates_string_dup_check:
                    dates_string_dup_check.append(date)
                    dates.append(datetime.strptime(date, '%m/%d/%Y').date())
                    self.log += "Extracted dates from headlines: {}. Awesome!\n".format(dates)
            else:
                self.log += "Found no dates in headlines. Boohoo.\n"
            dates.sort()
        return dates
    
    def calc_freq(self, dates: list) -> float:
        '''Calculate the frequency of PRs (as PRs per day).'''
        if dates is None:
            return None
        num_dates = len(dates)
        if num_dates < 2:
            return None
        # Need to calc distance between start and end date, and divide by number of dates
        oldest = dates[0]
        newest = dates[-1]
        delta = newest - oldest
        return num_dates / delta.days
        # freq = occurences / days = avg occurences / day.
        # Mult by 7 for avg occurences per week
    
    def expected_date_of_next_pr(self, dates, freq):
        '''
        Returns the expected date of next PR.
        This is accomplished by adding the average number of days between PRs to the last PR date.
        '''
        if dates is None or freq is None:
            return None

        newest = dates[-1]
        avg_days_between_pr = 1 / freq
        return newest + timedelta(days=avg_days_between_pr)
    
    def expected_days_until_next_pr(self, ednpr):
        '''Returns the expected number of days until next PR.'''
        if ednpr is None:
            return None
        
        today = date.today()
        delta = ednpr - today
        return delta.days

    def days_since_last_pr(self, dates):
        if dates is None:
            return None
        today = date.today()
        delta = today - dates[-1]
        return delta.days

    def analyze(self):
        self.analysis['dates'] = self.get_dates_from_headlines(self.headlines)
        self.analysis['freq'] = self.calc_freq(self.analysis['dates'])
        self.analysis['ednpr'] = self.expected_date_of_next_pr(self.analysis['dates'], self.analysis['freq'])
        self.analysis['edunpr'] = self.expected_days_until_next_pr(self.analysis['ednpr'])
        self.analysis['dslpr'] = self.days_since_last_pr(self.analysis['dates'])

        return self.analysis