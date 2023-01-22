import requests, re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from time import mktime
from io import BytesIO

def header_func():
    hdrs =  {
            "scheme": "https",
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "Connection": "keep-alive",
            "Expires": "-1",
            "Upgrade-Insecure-Requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64)"}
    return hdrs

def getData(stock):
    with requests.session():
        urlYFinance = 'https://finance.yahoo.com/quote/{}'
        h = header_func()
        website = requests.get(urlYFinance.format(stock), headers=h)
        soup = BeautifulSoup(website.text, 'html.parser')

        price = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text
        
        totalChange = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text

        percentChange = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text
        
        volume = soup.find('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)'}).find_all('tr')[7].text
        volume = volume.replace('Avg. Volume', '')
        return price, totalChange, percentChange

