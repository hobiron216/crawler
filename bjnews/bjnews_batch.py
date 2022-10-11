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

class BjNews:

    def create_folder(self, crawl_date, category):
        Path("/dataph/requests/news/bjnews/batch/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path("/dataph/requests/news/bjnews/batch/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://bjnews.com.cn/"
        self.a = 0
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []

    def get_items(self):
        categorys = ['opinion', 'news', 'world', 'finance']
        for category in categorys:
            page=0
        
            while True:
                crawl_date = self.crawl_date()
                self.create_folder(crawl_date,category)
                page = page + 1

                url = self.base_link + category + "/?page=" + str(page)
                while True:
                    try:
                        r = requests.get(url, timeout=50, proxies=self.proxies)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                html=r.text
                soup=BeautifulSoup(html,'html.parser')
                divs=soup.find_all("li")
                
                if "没有找到数据" in html:
                    break

                a=0
                for i,div in enumerate(divs):
                    a=a+1
                    # if a>40: #daily
                    #     break
                    try :
                        href = div.find("a").attrs.get('href')
                        self.list_link.append(href)
                    except:
                        break

                self.parser(self.list_link , crawl_date , category , page)
                del self.list_link[:]
    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:
            self.a = self.a + 1
            while True:
                try:
                    r = requests.get(url, timeout=50, proxies=self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text

            soup = BeautifulSoup(html, "html.parser")
            title= soup.find("div", class_="title").get_text()
            article = soup.find("div", class_="content").get_text()
            ndate = soup.find("span", class_="date").get_text()

            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            path_html = "/dataph/requests/news/bjnews/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

            result = {

                "title": title,
                "article": article,
                "ndate": ndate,
                "category": category,
                "crawl_date": crawl_date,
                "path_html": path_html,
                "url": url

            }
            #print (result)
            with open("/dataph/requests/news/bjnews/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                outfile.write(str(soup))
            with open("/dataph/requests/news/bjnews/batch/json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                outfile.write(str(result))
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(page))
            print("url : " + url)

BjNews().get_items()
