### BEGIN IMPORT PORTION OF SCRIPT ###
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
from datetime import datetime, date,timedelta, time as timepart #notice I am importing time from datetime as timepart to deconflict with the time module import
import os.path
import random
from bs4 import BeautifulSoup as soup
import sys
from textblob import TextBlob
### END IMPORT PORTION OF SCRIPT ###

##Start time of script
nowDTG = datetime.now().replace(microsecond=0)
print('Script started at: ' + str(nowDTG))

### BEGIN FUNCTION DEFINITION PORTION OF SCRIPT ###
def write_data_to_file(fname,data):
    f=open(fname,'w')
    f.write(str(data))
    f.close()
    return

def numTwitsOnPage(webPage):
    return len(getTwits(webPage))

def oldestTwitOnPage(webPage):
    try:
        oldestTwitTime = datetime.strptime(re.sub(r'(\w+\s\d{1,2})...\s(.+)',r'\1 \2', webPage.find_elements_by_xpath('//a[contains(@class, "MessageStreamView__created-at")]')[-1].text) +' '+str(2018), '%b %d %I:%M %p %Y')
    except:
        driver.find_element_by_xpath('//div[contains(@class,"bx-wrap")]//a[contains(@class, "bx-close-inside")]').click()
        oldestTwitTime = datetime.strptime(re.sub(r'(\w+\s\d{1,2})...\s(.+)',r'\1 \2', webPage.find_elements_by_xpath('//a[contains(@class, "MessageStreamView__created-at")]')[-1].text) +' '+str(2018), '%b %d %I:%M %p %Y')
    if (oldestTwitTime > nowDTG):
        oldestTwitTime = oldestTwitTime - timedelta(days=365)
    return oldestTwitTime

def getTwits(webPage):
    return webPage.find_elements_by_xpath('//div[contains(@class, "MessageList__item")]')

def updatePage(webPage):
    currentTwits = numTwitsOnPage(webPage)
    #webPage.send_keys(Keys.END)
    #webPage.send_keys(Keys.PAGE_DOWN)
    try:
        time.sleep((random.randrange(5, 9, 1))*0.1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep((random.randrange(2, 5, 1))*0.1)
    except:
        time.sleep((random.randrange(10, 20, 1))*0.1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            time.sleep((random.randrange(10, 20, 1))*0.1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            time.sleep((random.randrange(10, 20, 1))*0.1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep((random.randrange(10, 20, 1))*0.1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                time.sleep((random.randrange(10, 20, 1))*0.1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    time.sleep((random.randrange(10, 20, 1))*0.1)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except:
                    time.sleep((random.randrange(10, 20, 1))*0.1)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #while True:
    #    if(currentTwits != numTwitsOnPage(webPage)):
    #        break

def getPageBody(driver):
    return driver.find_element_by_tag_name('body')

def scroller(driver, twitLimit=False, dateLimit=False):
    webPage = driver.find_element_by_tag_name('body')
    #print(numTwitsOnPage(webPage))
    if (numTwitsOnPage(webPage) == 0):
        print('No twits found in this page')
    else:
        if (twitLimit==False and dateLimit==False):
            print('You should specify at least one argument between twitLimit and dateLimit')
            return
        elif (twitLimit!=False and dateLimit==False):
            while (numTwitsOnPage(webPage) <= twitLimit):
                updatePage(webPage)
        elif (twitLimit==False and dateLimit!=False):
            while (dateLimit < oldestTwitOnPage(webPage)):
                updatePage(webPage)
        else: #both are set
            while (dateLimit < oldestTwitOnPage(webPage) and numTwitsOnPage(webPage) <= twitLimit):
                updatePage(webPage)

### END FUNCTION DEFINITION PORTION OF SCRIPT ###

### Driver

webDriverLocation = r'/usr/local/bin/chromedriver'

seleniumHeadless = False
browser = 'chrome'

if seleniumHeadless:
    if (browser == 'chrome'):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--disable-notifications")
        options.add_argument("--dns-prefetch-disable")
        driver = webdriver.Chrome(executable_path=webDriverLocation, chrome_options=options) #hidden browser (lighter on resources)
    elif (browser == 'firefox'):
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(firefox_options=options, executable_path=webDriverLocation)
    else:
        print('You need to specify a webdriver to use')
        sys.exit()
else:
    if (browser == 'chrome'):
        from selenium.webdriver.chrome.options import Options                                                                                                                         
        options = Options()
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(executable_path=webDriverLocation, chrome_options=options) #unhidden browser (so you can watch what is happening)
    elif (browser == 'firefox'):
        driver = webdriver.Firefox(executable_path=webDriverLocation)
    else:
        print('You need to specify a webdriver to use')
        sys.exit()


# read from file and form baseUrl for looping

fname = 'Nasdaq1.csv'
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
            tick = line.split(',')[0]
            baseUrl=('https://stocktwits.com/symbol/'+tick)
            driver.get(baseUrl)
            stopDTG = datetime.combine(date(2018,4,1),timepart(12,0)) # when building your date here, the date function takes in four digit year, month and day (do not use leading zeros) and the time funciton takes in hour (24hour clock) and minutes
            scroller(driver, dateLimit=stopDTG)

            pageSource = driver.page_source
            data = pageSource.encode('utf-8')
            #print(data)
            savefname=(tick+'.txt')
            #write_data_to_file(savefname,data)
            print("File Write Done")
            # Let's turn the pageSource into something BeautifulSoup can handle (soupify it)
            pageSoup = soup(pageSource, 'html.parser')
            
            # Grab all of the tweets out of the soupified pageSoup
            #//div[contains(@class, "MessageList__item___1m1w9")]
            #Stwits = pageSoup.findAll('div', {'class': 'MessageList__item___1m1w9'})
            Stwits = pageSoup.findAll('div', {'class': 'MessageStreamView__message___2o0za'})
            #print(Stwits)
            #outPutFile=(tick+'.csv')
            outPutFile = ('/Users/manoranjankumar/Desktop/ProjectWork/stocktwits_csv/'+tick+'_stocktwits.csv')
            with open(outPutFile, 'w') as mycsv:
                for twit in Stwits:
                    #print(nowDTG)
                    try:
                        twitHeadData = twit.find('div', {'class': 'MessageStreamView__column___29E11'}).find('div', {'class': 'MessageStreamView__header___2q3fd'}).find('span', {'class': 'UserProfileLink__container___2JY3s'}).find("a")
                        twitUID = re.sub("^/|/$", "", twitHeadData['href'])
                    except:
                        twitUID = None
                    #print(twitUID)
                    try:
                        twitSentiment = twit.find('div', {'class': 'MessageStreamView__avatarContainer___35HD9'}).find('span', {'class': 'MessageStreamView__sentiment___11GoB'}).text
                    except:
                        twitSentiment = None
                    #print(twitSentiment)
                    try:
                        #twitUTIME = twit.find('div', {'class': 'MessageStreamView__header___2q3fd'}).find('a', {'class': 'MessageStreamView__created-at___HsSv2'}).text
                        twitTIME = datetime.strptime(re.sub(r'(\w+\s\d{1,2})...\s(.+)',r'\1 \2', twit.find('div', {'class': 'MessageStreamView__column___29E11'}).find('div', {'class': 'MessageStreamView__header___2q3fd'}).find('a', {'class': 'MessageStreamView__created-at___HsSv2'}).text) +' '+str(2018), '%b %d %I:%M %p %Y') 
                        # Fix last year time to last year part
                        if (twitTIME > nowDTG):
                            twitTIME = twitTIME - timedelta(days=365)
                    except:
                        twitTIME = None
                    #print(twitTIME)
                    try:
                        twitBodyData = twit.find('div', {'class': 'MessageStreamView__column___29E11'}).find('div', {'class': 'MessageStreamView__body___2giLh'}).find('span', {'type': 'cashtag'}).find("a")
                        twitID = twitBodyData['id']
                        twitTICK = twitID.split('-')[0]
                    except:
                        twitBodyData = None
                        twitID = None
                        twitTICK = None
                    #print(twitID)
                    try:
                        twitURL = twit.find('div', {'class': 'MessageStreamView__column___29E11'}).find('div', {'class': 'MessageStreamView__body___2giLh'}).find('span', {'type': 'url'}).find("a")
                        twitHREF=twitURL['href']
                    except:
                        twitHREF=None
                    #print(twitHREF)
                    try:
                        twitText = twit.find('div', {'class': 'MessageStreamView__column___29E11'}).find('div', {'class': 'MessageStreamView__body___2giLh'}).text.encode('utf-8','ignore').decode('utf-8')
                        #print(twitText)
                        #clean href links remove urls
                        twitText = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', twitText)        
                        # Fix classic tweet lingo
                        twitText = re.sub(r'\bthats\b', 'that is', twitText)
                        twitText = re.sub(r'\bive\b', 'i have', twitText)
                        twitText = re.sub(r'\bim\b', 'i am', twitText)
                        twitText = re.sub(r'\bya\b', 'yeah', twitText)
                        twitText = re.sub(r'\bcant\b', 'can not', twitText)
                        twitText = re.sub(r'\bwont\b', 'will not', twitText)
                        twitText = re.sub(r'\bid\b', 'i would', twitText)
                        twitText = re.sub(r'wtf', 'what the fuck', twitText)
                        twitText = re.sub(r'\bwth\b', 'what the hell', twitText)
                        twitText = re.sub(r'\br\b', 'are', twitText)
                        twitText = re.sub(r'\bu\b', 'you', twitText)
                        twitText = re.sub(r'\bk\b', 'OK', twitText)
                        twitText = re.sub(r'\bsux\b', 'sucks', twitText)
                        twitText = re.sub(r'\bno+\b', 'no', twitText)
                        twitText = re.sub(r'\bcoo+\b', 'cool', twitText)
                        # Convert to TextBlob
                        twitBlob = TextBlob(twitText)
                        #print(twitBlob)
                        #twitBlob = twitBlob.correct()
                        twitPolarity = float(twitBlob.sentiment.polarity)
                        twitSubjectivity = float(twitBlob.sentiment.subjectivity)
                        if twitPolarity >= 0.1:
                            twitTSentiment = 'Bullish'
                        elif twitPolarity <= -0.1:
                            twitTSentiment = 'Bearish'
                        else:
                            twitTSentiment = 'Neutral'
                    except:
                        twitText = ''
                        twitTSentiment = 'Neutral'
                        #print(twitText)
                        #print(twitTSentiment)
                    if twitUID and twitUID not in ('EstimizeAlerts' , 'ElliottwaveForecast' ,'marketchameleonwins','stockrow','ilovethestockmarket','IntegerInvestments','PPointTrading') and twitTICK == tick:
                        mycsv.write(','.join([str(nowDTG), str(twitTICK), str(twitUID), str(twitTIME), \
                             str(twitID), str(twitHREF), str(twitSentiment),str(twitTSentiment),str(round(twitPolarity,2)),\
                             str(round(twitSubjectivity,2)),str(twitText.replace(',','').replace('\n','').replace('\r',''))])+'\n')

driver.close()#close of chrome to able the opwning of new windows and to save source code.
driver.quit()
##END time of script
endDTG = datetime.now()
print('Script Ended at: ' + str(endDTG))
