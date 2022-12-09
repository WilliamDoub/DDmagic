from whoop_magus import WhoopMagus # scanning tool
from whoops import WhoopScan

class DDmagic():
    def __init__(self):
        self.summary = "DDmagic Summary:\n"
        self.whoop_magus = WhoopMagus()
    
    def run_whoop_magus(self):
        print("Available Whoops: " + self.whoop_magus.pretty_whoop_names_list(WhoopMagus.available_whoop_list))
        menu = {}
        i = 1
        for whoop_name in self.whoop_magus.available_whoop_dict:
            menu[str(i)] = whoop_name
            i += 1
        menu[str(i)] = "Quit"
        choice = ""
        # Display menu and get input selection
        while choice != str(i):
            print("Options: ")
            for c in menu:
                print("{0}: {1}".format(c, menu[c]))
            choice = input("Enter selction: ")
            i = 1
            for whoop_name in WhoopMagus.available_whoop_dict:
                if choice == str(i):
                    answer = input("Range for {}? (y/n): ".format(whoop_name))
                    whoop = WhoopMagus.available_whoop_dict[whoop_name]
                    if answer == "n":
                        self.whoop_magus.scan(whoop)
                    elif answer == "y":
                        start = int(input("Enter start index: "))
                        end = int(input("Enter end index: "))
                        self.whoop_magus.scan_range(whoop, start, end)
                i += 1
        print("Goodbye")
    
    def __str__(self):
        self.summary += str(self.whoop_magus)
        return self.summary


#scan_matrix??? could be cool

# Make pandas dataframe with whoopstock data. Can export to sheets/excel. Also consider MySQL database.
# Make WhoopMagus method to import dataframe and filter whoop scan results there by latest fundamentals 
# from otcmarkets.com quickly. FilterMagus?