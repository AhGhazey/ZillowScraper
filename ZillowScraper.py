import sys
import os
from Scraper import Zillow
import threading

import requests



def StartSpiders():
    try:
       
        scraper =  Zillow('https://www.zillow.com/homes/for_sale/0_fr/1_fs/37211_rid/0_singlestory/34.052659,-84.085236,33.439463,-85.023194_rect/X1-SS-1f8zzkxyf0zqt_52lx1_sse/','https://www.zillow.com','Atlanta')
        scraper.ScrapeData()
    except Exception:
        print ('error in running spiders')

if __name__ == '__main__':
    try:
        StartSpiders()
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

##nohup python CheckTrade.py &



def open_zillow ():
    url  = 'https://www.zillow.com' 
    session_request = requests.session()
    session_request.get(url)
    url_1 = 'https://www.zillow.com/homes/for_sale/0_fr/1_fs/37211_rid/0_singlestory/34.052659,-84.085236,33.439463,-85.023194_rect/X1-SS-1f8zzkxyf0zqt_52lx1_sse/'
    
    req_headers = {
    'referer': url,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    
    result_1 = session_request.get(url_1, headers = req_headers)

    print (result_1.content)
