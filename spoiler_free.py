import pandas as pd
import requests
import sys
import re
import random
from bs4 import BeautifulSoup
from tabulate import tabulate

# ----------------------------------------------------------------------------
# ---                       choose event                                   ---
# ----------------------------------------------------------------------------
event = 'UFC 250'
# event = 'UFC Fight Night: Ortega vs. The Korean Zombie'


# ----------------------------------------------------------------------------
# ---                       choose fighter                                 ---
# ----------------------------------------------------------------------------
fighter = 'Andre Ward'


# ----------------------------------------------------------------------------
def check_boxing_columns(rows):
    total = 0
    for row in rows:
        switch =  {
            'No.': True,
            'Result': True,
            'Record': True,
            'Opponent': True,
            'Round, time': True,
            'Type': True,
            'Method': True,
            'Date': True,
            'Location': True
        }
        if (switch.get(row,False)):
            total += 1
    # print("total: " + str(total) )
    # print(rows)
    if (total > 7):
        print("Boxer")
        return True
    return False

def check_mma_columns(rows):
    total = 0
    for row in rows:
        switch =  {
            'Res.': True,
            'Record': True,
            'Opponent': True,
            'Method':    True,
            'Event': True,
            'Date': True,
            'Round': True,
            'Time': True,
            'Location': True
        }
        if (switch.get(row,False)):
            total += 1

    if (total > 8):
        print("MMA Fighter")
        return True
    return False

def getUrl(fighter):
    if (fighter == ''):
        print("No Fighter Selected")
        exit()
    fighter.replace(' ', '_')
    url = 'https://en.wikipedia.org/wiki/'
    url += fighter
    return url

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


def getEvent():
    # --------------------------------------------------------------------------
    #                                  EVENT
    # --------------------------------------------------------------------------
    url = getEventUrl(event)
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    # result = soup.find_all('table', {'class': 'wikitable'})
    result = soup.find('table', {'class': 'toccolours'})
    if result is None:
        result = soup.find('table')
    if result is None:
        print("Table not found")
        sys.exit()
    td = result.find_all('tr')
    rows = [i.text.rstrip() for i in td]   # dont need this right now
    table = pd.read_html(result.prettify())[0]

    # Fix column names
    column_names = [i[1] for i in table.columns]
    column_names[1] = 'Fighter 1'
    column_names[2] = 'vs.'
    column_names[3] = 'Fighter 2'
    table.columns = column_names

    # Remove unwanted columns and change to 'vs.'
    table = table.drop(['Method','Round','Time','Notes'], axis=1)
    table['vs.'] = 'vs.'

    # Randomly choose which fighter is where
    for index, row in table.iterrows():
        x = row['Fighter 1']
        y = row['Fighter 2']
        if (random.choice([True,False])):
            row['Fighter 1'] = x
            row['Fighter 2'] = y
        else:
            row['Fighter 1'] = y
            row['Fighter 2'] = x


        # --- check what prelims there are ---
        has_prelim = table['Weight class'].str.contains("Preliminary")
        has_early_prelim_l = table['Weight class'].str.contains("Early Preliminary")
        has_early_prelim = any(i == True for i in has_early_prelim_l)

        # --- get range of tables
        prelim_row_i = list(has_prelim).index(True)
        if (has_early_prelim):
            early_prelim_row_i = list(has_early_prelim_l).index(True)
            prelim_row_e = early_prelim_row_i
        else:
            prelim_row_e = len(table)

        # --- split and print tables ---
        maincard = table.iloc[:prelim_row_i,:]
        print(tabulate([[event.replace('_',' ')]], tablefmt='psql'))
        print(tabulate([["Maincard"]], tablefmt='psql'))
        print(tabulate(maincard,headers='keys',tablefmt='psql',showindex=False))

        prelims  = table.iloc[prelim_row_i+1:prelim_row_e,:]
        print(tabulate([["Prelims"]], tablefmt='psql'))
        print(tabulate(prelims,headers='keys',tablefmt='psql',showindex=False))

        if (has_early_prelim):
            early_prelims  = table.iloc[early_prelim_row_i+1:,:]
            print(tabulate([["Early Prelims"]], tablefmt='psql'))
            print(tabulate(early_prelims,headers='keys',tablefmt='psql',
                           showindex=False))

        sys.exit()

# run event if in command line
if (len(sys.argv) > 1):
    if (sys.argv[1] == 'event'):
        getEvent()
    sys.exit()



# ----------------------------------------------------------------------------
#                              FIGHTER SCHEDULE
# ----------------------------------------------------------------------------

req = requests.get(getUrl(fighter)).text
soup = BeautifulSoup(req, 'lxml')
result = soup.find_all('table', {'class': 'wikitable'})

for res in result:
    tr = res.find('tr')
    td = tr.find_all('th')
    rows = [i.text.rstrip() for i in td]
    # print(rows)
    if (check_boxing_columns(rows)):
        table = pd.read_html(res.prettify())[0]
        q = table[['No.', 'Opponent', 'Date']]
    elif (check_mma_columns(rows)):
        table = pd.read_html(res.prettify())[0]
        q = table[['Opponent', 'Event', 'Date']].copy().dropna()
        q.insert(0, '', list(range(len(q.index),0,-1)))
        new_date = pd.to_datetime(q['Date']).dt.strftime('%m.%d.%Y')
        q.loc[:,'Date'] = new_date
        shorten_lambda = lambda x: x[0:x.find(':')] if (x.find(':')>0) else x
        q.loc[:,'Event'] = q[['Event']].applymap(shorten_lambda)


print(tabulate([[fighter.replace('_',' ')]], tablefmt='psql'))
print(tabulate(q,headers='keys',tablefmt='psql',showindex=False))
