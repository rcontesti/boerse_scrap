


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
import requests
#-------------------------------------------------------------------------------


urls=['http://en.boerse-frankfurt.de/searchresults?_search=argentinien&p=1',
'http://en.boerse-frankfurt.de/searchresults?_search=argentinien&p=2']


r  = requests.get(url)
xpath="""//*[@id="main-wrapper"]/div[5]/div/div/div[2]/div[2]/table"""


soup = BeautifulSoup(data.text,'lxml').findAll('')
trs=BeautifulSoup(html,'lxml').find('table', {'class':"table"}).findAll('tr')

print(trs)

"""for tr in trs:
    row=[]
    for td in tr.findAll('td')[0:5]: row.append(td.text)
    if len(row)>0:table.append(row)"""
