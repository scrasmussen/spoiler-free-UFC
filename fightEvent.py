import sys

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import re
import random



def getEventUrl(event):
    if (event == ''):
        print("No Event Selected")
        exit()
    event = event.replace(' ', '_')

    #- check if UFC PPV
    p = re.compile('UFC_[0-9]+')
    match = p.match(event)
    if match is not None:
        event = match.group()

    url = 'https://en.wikipedia.org/wiki/'
    url += event
    return url

def print_title(name):
    print(tabulate([[name]], tablefmt='psql'))

def print_card(card):
    print(tabulate(card, headers='keys',tablefmt='psql',showindex=False))

def fix_column_names(names):
    # Fix column names
    column_names = [i[1] for i in names]
    column_names[1] = 'Fighter 1'
    column_names[2] = 'vs.'
    column_names[3] = 'Fighter 2'
    return column_names




class FightEvent:
    def print_name(self):
        print_title(self.name)

    def print_events(self):
        print_title("Maincard")
        print_card(self.maincard)

        print_title("Prelims")
        print_card(self.prelims)

        if self.early_prelims is not None:
            print_title("Early Prelims")
            print_card(self.early_prelims)


    def get_table(self, soup):
        result = soup.find('table', {'class': 'toccolours'})
        if result is None:
            print("Table not found")
            sys.exit()
        td = result.find_all('tr')
        rows = [i.text.rstrip() for i in td]   # dont need this right now
        table = pd.read_html(result.prettify())[0]

        # Fix column names
        table.columns = fix_column_names(table.columns)
        # Remove unwanted columns and change to 'vs.'
        table = table.drop(['Method','Round','Time','Notes'], axis=1)
        table['vs.'] = 'vs.'

        for index, row in table.iterrows():
            x = row['Fighter 1']
            y = row['Fighter 2']
            if (random.choice([True,False])):
                row['Fighter 1'] = x
                row['Fighter 2'] = y
            else:
                row['Fighter 1'] = y
                row['Fighter 2'] = x

        self.table = table


    def sort_table(self):
        # prelims
        has_prelim = self.table['Weight class'].str.contains('Preliminary')
        prelim_row_i = list(has_prelim).index(True)

        # early prelims
        has_early_prelim = self.table['Weight class'].str.contains(
            "Early Preliminary")
        if (any(has_early_prelim)):
            early_prelim_row_i = list(has_early_prelim).index(True)
            prelim_row_end = early_prelim_row_i
        else:
            prelim_row_end = len(self.table)

        self.maincard = self.table.iloc[:prelim_row_i,:]
        self.prelims  = self.table.iloc[prelim_row_i+1:prelim_row_end,:]
        if (any(has_early_prelim)):
            self.early_prelims = self.table.iloc[early_prelim_row_i+1:,:]
        else:
            self.early_prelims = None


    def __init__(self, name):
        self.name = name.replace('_',' ')

        req = requests.get(getEventUrl(name)).text
        soup = BeautifulSoup(req, 'lxml')

        self.get_table(soup)
        self.sort_table()

        # self.mma_record = get_record(soup, 'mma')
        # self.boxing_record = get_record(soup, 'boxing')
