import hashlib
import json
import requests
from pathlib import Path
from logger import Logger
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from selenium import webdriver
from pyvirtualdisplay import Display

class Cn_News:

    def create_folder(self, crawl_date, category):
        Path("/dataph/requests/news/china_news/batch/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path("/dataph/requests/news/china_news/batch/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def trim_word(self,word, from_start=0, from_end=0):
        return word[from_start:len(word) - from_end]

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://www.chinanews.com/"
        self.a = 0
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []
        self.display = Display(visible=0, size=(1366, 768))
        self.display.start()

    def get_browser(self):
        browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        browser.maximize_window()
        return browser

    def get_items(self):
        browser = self.get_browser()
        categorys = ['scroll-news', 'china', 'world', 'society', 'finance', 'business', 'fortune','auto', 'gangao', 'taiwan' , 'huaren', 'ent', 'sports', 'cul']
        for category in categorys:
            if category == 'scroll-news' :
                url= self.base_link + category
                self.get_html_soup(category, url)

            else :
                crawl_date = self.crawl_date()
                url=self.base_link + category
                self.create_folder(crawl_date, category)
                browser.get(url)
                page="click scroll"
                
                while True:
                    try:
                        browser.find_element_by_id("page_bar0").click()
                        #time.sleep(1)
                    except:
                        break
                html=browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                divs = soup.findAll("div", class_="bigpic_list")
                for div in divs:
                    href=div.find("a").attrs.get("href")
                    if "http:" not in href:
                        href="http:"+href

                    self.list_link.append(href)
                self.parser(self.list_link,crawl_date,category,page)
                del self.list_link[:]
        browser.close()
        self.display.stop()
    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:
            self.a = self.a + 1
            b = True
            # if len(url)<45:
            #     continue
            print("url : " + url)
            if "tp/hd" in url or "shipin" in url:
            	continue
            while b:
                try:
                    r = requests.get(url, timeout=50, proxies=self.proxies)
                    b = False
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text

            soup = BeautifulSoup(html, "html.parser")
            title= soup.find("h1", attrs={"style":"display:block; position:relative; clear:both"}).get_text()
            article = soup.find("div", class_="left_zw").get_text()
            ndate = soup.find("div", class_="left-t").get_text().split("来")#split
            ndate =ndate[0]

            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            path_html = "/dataph/requests/news/china_news/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

            result = {

                "title": title,
                "article": article,
                "ndate": ndate,
                "category": category,
                "crawl_date": crawl_date,
                "path_html": path_html,
                "url": url

            }
            # print (result)
            with open("/dataph/requests/news/china_news/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                outfile.write(str(soup))
            with open("/dataph/requests/news/china_news/batch/json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                outfile.write(str(result))
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(page))
            
            

    def get_html_soup(self,category,url):
        crawl_date=self.crawl_date()
        self.create_folder(crawl_date, category)
        page = "num-page"
        for j in range(1,11):
            url = url + "/news" + str(j) + ".html"
            while True:
                    try:
                        r = requests.get(url, timeout=50, proxies=self.proxies)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion html_soup timeout")
                        continue
            html=r.text
            soup=BeautifulSoup(html,'html.parser')
            divs=soup.find_all("div", class_="dd_bt")

            a=0
            for i,div in enumerate(divs):
                a=a+1
                # if a==1:
                #     continue
                # if a>40: #daily
                #     break
                href = div.find("a").attrs.get('href')
                href= "http:" + href
                self.list_link.append(href)
            #print(self.list_link)
            

        self.parser(self.list_link,crawl_date,category,page)
        del self.list_link[:]




Cn_News().get_items()
