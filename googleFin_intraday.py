import csv
import datetime
import re
import codecs
import urllib.request
import urllib.parse
import pandas as pd
import os.path
from bs4 import BeautifulSoup
import pytz

import os

#timezone set
#server_timezone = pytz.timezone("US/Eastern")

os.environ['TZ'] = 'US/Eastern'

# REQUIRED
def getsource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    page_html=uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    page_soup=BeautifulSoup(page_html,"html.parser")
    return [page_soup, page_html]

def get_google_finance_intraday(ticker, period=60, days=1, exchange='NASD'):
    # build url
    url = 'https://finance.google.com/finance/getprices' + \
          '?p={days}d&f=d,o,h,l,c,v&q={ticker}&i={period}&x={exchange}'.format(ticker=ticker, period=period, days=days, exchange=exchange)
    #page = requests.get(url)
    page = getsource(url)
    pagedata=(page[1])
    #reader = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))
    reader = csv.reader(codecs.iterdecode(pagedata.splitlines(), "utf-8"))
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))
    if len(rows):
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'), columns=columns)
    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))

# input data
#ticker = 'MSFT'
period = 3600
days = 25
exchange = 'NASD'

fname = 'Nasdaq.csv'
flagheader = 'Y'

if not os.path.isfile(fname):
    print ('File does not exist.')
else:
    with open(fname) as f:
        if str(flagheader) == 'Y':
            firstLine = f.readline()
            content = f.read().splitlines()
        else:
            print('no headers')
            content = f.read().splitlines()
        for line in content:
            ticker = line.split(',')[0]
            outPutFile=(ticker+'_googleintra.csv')
            with open(outPutFile, 'w') as mycsv:
                df = get_google_finance_intraday(ticker, period=period, days=days)
                df.to_csv(outPutFile, sep=',', encoding='utf-8')
del os.environ['TZ']
