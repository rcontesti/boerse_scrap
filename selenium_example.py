#
"""
La idea es meter una serie de precios de bonos en un diccionario:

prices={"BP28": Dataframe(), "...": ...}

#TODO: La pagina demora al proposito la carga de los precios historicos asi no
los scrapeo. Funciono las primeras veces y despues demora cada vez mas.
Seguramente por un tema de IP
""""


#-------------------------------------------------------------------------------
#--LIBRARIES--------------------------------------------------------------------
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pickle
import pandas as pd

#-------------------------------------------------------------------------------
#--FUNCTIONS--------------------------------------------------------------------
#-------------------------------------------------------------------------------

def test_browser(url, driver_loc):
    xpath="""//*[@id="grid-table-47006002"]/div/table/tbody/tr[1]/td[2]"""
    xpath="""//*[@id="historic-price-list"]/div/div[1]/div/h2/span"""

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(driver_loc)
    #browser = webdriver.Chrome(driver_loc, chrome_options=chrome_options)
    browser.get(url)
    delay = 30 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print ("Page is ready!")
    except TimeoutException:
        html = browser.page_source
        print ("Loading took too much time!")
    browser.close()
    return html

def get_url(bond_url, first_date, last_date):
    return "http://en.boerse-frankfurt.de/bonds/pricehistory/"\
    +bond_url\
    +"/FSE/"\
    +first_date\
    +"_"\
    +last_date\
    +"Price_History"

def get_prices(html):
    table=[]
    trs=BeautifulSoup(html,'lxml').find('div',{'id':"historic-price-list"}).find('table', {'class':"table"}).findAll('tr')
    for tr in trs:
        row=[]
        for td in tr.findAll('td')[0:5]: row.append(td.text)
        if len(row)>0:table.append(row)


    return pd.DataFrame(table, columns=['Date','Open','High','Low', 'Close'])


#-------------------------------------------------------------------------------
#--PARAMS-----------------------------------------------------------------------
#-------------------------------------------------------------------------------

driver_loc='/home/rcontesti/Downloads/chromedriver'

bond_url="Buenos_Aires-_Province_ofDL-Notes_200726-28_RegS-Bond-2028-XS0290125391"
#bond_url='Buenos_Aires-_Province_ofDL-Bonds_200618_RegS-Bond-2018-XS0270992380'
first_date="3.7.2018"
last_date="12.8.2018"



#-------------------------------------------------------------------------------
url=get_url(bond_url, first_date, last_date)
html=test_browser(url, driver_loc)
pickle.dump(html, open('html.p', 'wb'))
html=pickle.load(open('html.p', 'rb'))
prices=get_prices(html)

print(url)
print(prices.head())
