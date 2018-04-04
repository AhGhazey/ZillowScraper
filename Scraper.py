__author__ = 'aghazey'
from house import House
import time
import requests
from random import randint
from lxml import html
import os, errno
import urllib
import gc
import Configuration
from bs4 import BeautifulSoup
import gzip
from datetime import datetime, timedelta
import re
class Zillow():
    """description of class"""
    def __init__(self, url, baseurl, location = None):
        self.url = url
        self._base_url = baseurl
        self.Location = location
        self.prev_url = self._base_url
        self.request_session = requests.session()
        self.req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.request_session.get(self._base_url)


    def ScrapeData(self):
        paginated_url = self.__process_url(self.url)
        while paginated_url:
            self.sleep_script(5, 9)
            paginated_url = self.__process_url(paginated_url)

    def sleep_script(self,mini, maxi):
        script_sleep = randint(mini, maxi)
        print ('Script is going to sleep for %d seconds.' % script_sleep)
        time.sleep(script_sleep)

    def __process_url(self, url):
        """
        :param url:
        :return:
        """
        try:
            print('============= URL: ' + url + ' ==============')
            data = self.fetchData(url,self.prev_url)
            if not data:
                print('No data grabbed.')
                return None
            soup = BeautifulSoup(data, 'lxml')
            if not soup:
                print('Invalid bs4 object')
                return None

            # try to get all house links
            house_links = soup.select('a.zsg-photo-card-overlay-link')
            if not house_links or len(house_links) == 0:
                print('No link found!')
                return None

            # enumerate all houses details link to get house details
            for house_link in enumerate([link for link in house_links if link.has_attr('href')]):
                house_url = house_link[1].get('href')
                if self.__url_exists(house_url) or '/community' in house_url :
                    print ('House URL: %s already exists.\nSkip this url...' % house_url)
                    continue
                self.__get_house_details(self._base_url + house_url+'?fullpage=true')
                #script sleep to simulate human being
                self.sleep_script(1, 10)
            #pagination    
            next_partial_url_link = soup.select_one('.zsg-pagination-next a')
            if next_partial_url_link == None:
                return None
            next_page_url = self._base_url + next_partial_url_link['href']
            self.prev_url = url
            return next_page_url  
                 
        except Exception:
            print('Error process results' )
            return None
        return None

    def fetchData(self, url, referer = None):
        try:
            self.req_headers['referer'] = self.prev_url
            result = self.request_session.get(url, headers = self.req_headers)
            if result.ok == False:
                return None
            data = result.content
            return data
        except Exception:
            print('Error in fetching data' )
            return None
        
        
        


    def __get_house_details(self, url):

        try:

            print('House URL: ' + url)
            data = self.fetchData(url)
            if not data:
                print('No data grabbed.')
                return

            soup = BeautifulSoup(data, 'lxml')
            if not soup:
                print('Invalid bs4 object.')
                return
            house = House()

            house.Url = url

            state = soup.select_one('#region-state a')
            if state != None:
                house.State= state.text.strip()

            city = soup.select_one('#region-city a')
            if city != None:
                house.City= city.text.strip()

            info =  soup.select_one('ol.zsg-breadcrumbs') #address id need to be tested 
            if info != None :
                if len(info) >=5:
                    address = info.select('li')[4]
                    children = address.findChildren()
                    for child in children:
                        house.PropertyAddress= address.text.strip()
                        break;
                    

            price =  soup.select_one('.main-row.home-summary-row span') #price id need to be tested 
            if price != None:
                house.Price = re.sub('[^0-9]','', price.text.strip()) 

            companyName = soup.select_one('.snl.company-name') #companyName id need to be tested 
            if companyName != None:
                house.CompanyName = companyName.text.strip()

            agentName = soup.select_one('.profile-name-link') #agentName id need to be tested 
            if agentName != None:
                house.AgentName = agentName.text.strip()
                agentProfileLink = self._base_url + agentName['href']
                house.AgentProfile = agentProfileLink
                #need deeper level to get licence number keep in mind 

            phoneNumber = soup.select_one('.snl.phone') #phoneNumber id need to be tested 
            if phoneNumber != None:
                house.PhoneNumber = phoneNumber.text.strip()


            
            facts = soup.select('ul.zsg-sm-1-1.hdp-fact-list li') #mlsNumber id need to be tested 
            try:
                if facts != None:
                    for li in facts:
                        factName = ''
                        factValue = ''
                        first_span = li.select_one('.hdp-fact-name')
                        second_span = li.select_one('.hdp-fact-value')
                        if first_span != None:
                            factName = first_span.text.strip()
                        if second_span !=  None:
                            factValue = second_span.text.strip()

                        if factName == 'MLS #:':
                            house.MLSNumber = factValue
                        elif factName == 'Days on Zillow:':
                            days =  factValue
                            days_to_subtract = int(re.sub('[^0-9]','', days))
                            published_date = datetime.today() - timedelta(days=days_to_subtract)
                            house.Date = '{0.month}/{0.day}/{0.year}'.format(published_date) 
            except Exception:
                print('Error when getting house details')
            self._write_house(house.getHouseString())

            self._write_on_mf(url)
            




        except Exception:
            print('Error when getting house details')
            return False

    def __url_exists(self, url):
        """
        :param url:
        :return: True if url found inside mf otherwise False
        """
        
        try:
            file_exists = os.path.isfile('ZillowHistory.txt') 
            if file_exists == False:
                open('ZillowHistory.txt', 'w')
                self.sleep_script(1,3)
            
            with open('ZillowHistory.txt', 'r') as f:
                for line in f:
                    if url in line:       
                        return True
        except Exception:
            print ('Error when search url inside zillow history file')
            return False
        return False

    def _write_on_mf(self, url):
       
        try:
            with open('ZillowHistory.txt', 'a') as f:
                f.write(url + '\n')
        except Exception:
            print ('Error when write url on zillow history' )
            return None

    def _write_house(self, data):
       
        try:
            file_exists = os.path.isfile('Zillow.csv') 
            if file_exists == False:
                with open('Zillow.csv', 'w') as file:
                    file.write('Creating')

            with open('Zillow.csv', 'a') as f:
                f.write(data)
        except Exception:
            print ('Error when write url on write house' )
            return None