#
"""
La idea es meter una serie de precios de bonos en un diccionario:

prices={"BP28": Dataframe(), "...": ...}

#TODO: La pagina demora al proposito la carga de los precios historicos asi no
los scrapeo. Funciono las primeras veces y despues demora cada vez mas.
Seguramente por un tema de IP
"""
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
    #browser = webdriver.Chrome(driver_loc)
    browser = webdriver.Chrome(driver_loc, chrome_options=chrome_options)
    print(url)
    browser.get(url)
    delay = 60 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print ("Page is ready!")
        html = browser.page_source
    except TimeoutException:
        print ("Loading took too much time!")
        html = None
    browser.close()
    return html

def get_url(bond_url, first_date, last_date):
    return "http://en.boerse-frankfurt.de/bonds/pricehistory/"\
    +bond_url\
    +"/FSE/"\
    +first_date\
    +"_"\
    +last_date\
    #+"Price_History"

def get_prices(html):
    table=[]
    trs=BeautifulSoup(html,'lxml').find('div',{'id':"historic-price-list"}).find('table', {'class':"table"}).findAll('tr')
    for tr in trs:
        row=[]
        for td in tr.findAll('td')[0:5]: row.append(td.text)
        if len(row)>0:table.append(row)
    return pd.DataFrame(table, columns=['Date','Open','High','Low', 'Close'])

def get_prices_dic(bond_urls, first_date, last_date):
    prices={}
    for bond,bond_url in bond_urls.items():
        url=get_url(bond_url, first_date, last_date)
        html=test_browser(url, driver_loc)
        if html!=None:
            prices[bond]=get_prices(html)
    return prices

def append_new_data(prices_new, prices_old):
    for key_new in prices_new.keys():
        if key_new not in prices_old.keys():
            prices_old[key_new]=prices_new[key_new]
        else:
            dates_old_min=prices_old[key_new]['Date'].min()
            dates_old_max=prices_old[key_new]['Date'].max()
            dates_new_min=prices_new[key_new]['Date'].min()
            dates_new_max=prices_new[key_new]['Date'].max()
            if dates_new_max>dates_old_max:
                new_part=prices_new[key_new][prices_new[key_new]['Date']>dates_old_max]
                prices_old[key_new]=pd.concat(prices_old[key_new], new_part)
            elif dates_new_min<dates_old_min:
                new_part=prices_new[key_new][prices_new[key_new]['Date']<dates_old_min]
                prices_old[key_new]=pd.concat(prices_old[key_new], new_part)
            else:
                pass
    pickle.dump(prices_old, open('prices.p', 'wb'))
#-------------------------------------------------------------------------------
#--PARAMS-----------------------------------------------------------------------
#-------------------------------------------------------------------------------

driver_loc='/home/rcontesti/Downloads/chromedriver'

bue_urls={
'BP28':"Buenos_Aires-_Province_ofDL-Notes_200726-28_RegS-Bond-2028-XS0290125391",
'BP18':"Buenos_Aires-_Province_ofDL-Bonds_200618_RegS-Bond-2018-XS0270992380"
}
gov_arg_bonds_urls={
'AE48': 'Argentinien-_RepublikDL-Bonds_201848-Bond-2048-US040114HR43',
'AA46': 'Argentinien-_RepublikDL-Bonds_1746_SerC_P1-Bond-2046-US040114GY03',
'AC17': 'Argentinien-_RepublikDL-Bonds_201717-2117_RegS-Bond-2117-USP04808AN44',
}
first_date="1.1.2013"
last_date="1.9.2018"
#-------------------------------------------------------------------------------
prices_new=get_prices_dic(bue_urls, first_date, last_date)
prices_old=pickle.load(open('prices.p', 'rb'))
append_new_data(prices_new, prices_old)



print(prices_old['BP28']['Date'].iloc[0])
print(prices_old['BP28']['Date'].iloc[-1])
