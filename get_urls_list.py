


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





bond_urls=[]
for url in urls:
    r  = requests.get(url)
    for table in BeautifulSoup(r.text,'lxml').findAll('table'):
        for row in table.findAll('tr'):
            for col in row.findAll('td'):
                for a in col.findAll('a', href=True):
                    if a.text:
                        if a['href'][0:8]=='/bonds/A':
                            bond_urls.append(a['href'])
