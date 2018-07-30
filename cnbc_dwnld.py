# REQUIRED
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import time
import random
import sys
# REQUIRED
def getsource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    page_html=uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    page_soup=BeautifulSoup(page_html,"html.parser")
    return [page_soup, page_html]

# REQUIRED
def write_dict_to_csv(fname,header,data):
    f=open(fname,'w')
    f.write(header)
    #f.write('\n')
    for item in data:
        for elem in item:
            f.write(elem)
            #f.write(' , ')# excel change of column
        #f.write('\n')   # excel change of line
    f.close()
    return

def write_data_to_file(fname,data):
    f=open(fname,'w')
    f.write(str(data))
    f.close()
    return

#Get Nasdaq 100 stocks list
nasurl="https://www.cnbc.com/nasdaq-100/"
nasdaqStocks = getsource(nasurl)
nasdaqStocksdata=(nasdaqStocks[0])

table1 = nasdaqStocksdata.findChildren('table')[0]
table2 = nasdaqStocksdata.findChildren('table')[1]

rows1 = table1.findChildren('tr')
rows2 = table2.findChildren('tr')
rows = rows1 + rows2
#print(rows)

datasets = []
for row in rows:
    #print(row)
    #time.sleep(2)
    cells = row.findChildren('td', attrs={'class' : 'first text'})
    for cell in cells:
        cell_content = cell.getText()
        clean_content = re.sub('\s+', ' ', cell_content).strip()
        #print(clean_content)
        href_content=cell.find('a').get('href')
        href_content = 'https://'+re.sub('\s+', ' ', href_content).strip().split('//')[-1]
        #print(href_content)
        cnn_href = 'http://money.cnn.com/quote/quote.html?symb='+clean_content
        try:
            indcheck= getsource(cnn_href)
            indcheckdata = (indcheck[0])
            sector = indcheckdata.find('table', attrs={'class' : 'wsod_dataTable wsod_dataTableBig wsod_quoteProfileModule'}).find('div', attrs={'class' : 'wsod_fRight wsod_bold'}).text
            industry = indcheckdata.find('table', attrs={'class' : 'wsod_dataTable wsod_dataTableBig wsod_quoteProfileModule'}).findChildren('div', attrs={'class' : 'wsod_fRight wsod_bold'})[1].text
            #print(industry)
            #indcheckdata.find( "table", {"id":"ctl00_MainBody_PublicForms_gvForms"} ).findChildren('a')
            #sectable = indcheckdata.find('table', {"class":"'table table-nv m-b-0'"})
            #sectable = indcheckdata.find('table', attrs={'class' : 'table table-nv m-b-0'})
            #print(sectable)
            time.sleep((random.randrange(2, 4, 1))*0.1)
            #print(sectable)
            #print(indcheckdata)
            #write_data_to_file('xyztest.txt', sectable)
            #print("manumanumanumanumanu")
        except:
            sector = ''
            industry = ''
        new_content='\n'+clean_content+','+sector+','+industry+','+href_content+','+cnn_href
        #print(new_content)
        datasets.append(new_content)

write_dict_to_csv('NasdaqNew.csv','SYMBOL,SECTOR,INDUSTRY,CNBC_LINK,CNN_LINK',datasets)
