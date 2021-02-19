import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

def getUrl(fighter):
    if (fighter == ''):
        print("No Fighter Selected")
        exit()
    fighter.replace(' ', '_')
    url = 'https://en.wikipedia.org/wiki/'
    url += fighter
    return url

def get_record(soup, record_type):
    if (record_type == 'boxing'):
        columns = ['No.', 'Opponent', 'Date']
        record_name = 'Professional boxing record'
    if (record_type == 'mma'):
        columns = ['Opponent', 'Event', 'Date']
        record_name = 'Mixed martial arts record'

    headers = soup.select_one('h2:contains("'+record_name+'")')
    if (headers is None):
        return None
    h_table = headers.find_next_sibling()
    row = h_table.find_next_sibling()
    row_text = row.get_text()

    if ('Record' in row_text) and ('Opponent' in row_text):
        table = pd.read_html(row.prettify())[0]
        record = table[columns].copy().dropna()
        # fix date
        new_date = pd.to_datetime(record['Date']).dt.strftime('%m.%d.%Y')
        record.loc[:,'Date'] = new_date
        if (record_type == 'mma'):
            record.insert(0, '', list(range(len(record.index),0,-1)))
            # shorten event name
            shorten_lambda = lambda x: x[0:x.find(':')] \
                if (x.find(':')>0) else x
            record.loc[:,'Event'] = record[['Event']].applymap(shorten_lambda)
        return record
    return None



class Fighter:
    def print_name(self):
        print(tabulate([[self.name]], tablefmt='psql'))
    def print_records(self):
        if (self.mma_record is not None):
            print(tabulate(self.mma_record,headers='keys',tablefmt='psql',
                           showindex=False))
        if (self.boxing_record is not None):
            print(tabulate(self.boxing_record,headers='keys',tablefmt='psql',
                           showindex=False))

    def __init__(self, name):
        self.name = name.replace('_',' ')

        req = requests.get(getUrl(name)).text
        soup = BeautifulSoup(req, 'lxml')

        self.mma_record = get_record(soup, 'mma')
        self.boxing_record = get_record(soup, 'boxing')
