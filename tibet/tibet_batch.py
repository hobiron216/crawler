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

class Tibet:

    def create_folder(self, crawl_date, category):
        Path("/dataph/requests/news/tibet/batch/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path("/dataph/requests/news/tibet/batch/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://tibet.cn/cn/"
        self.a = 0
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []

    def get_items(self):
        categorys = ['politics', 'bwsp', 'aid_tibet', 'religion', 'fp']
        for category in categorys:
            page=-1

            while True:
                crawl_date = self.crawl_date()
                self.create_folder(crawl_date,category)
                page = page + 1
                # if page > 4:
                #     break
                if page==0:
                    url = self.base_link + category
                else:
                    url = self.base_link + category + "/index_" + str(page) + ".html"

                while True:
                    try:
                        r = requests.get(url, timeout=50, proxies=self.proxies)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                html=r.text
                soup=BeautifulSoup(html,'html.parser')
                divs=soup.find_all("h4")

                if r.status_code == 404:
                    break

                a=0
                for i,div in enumerate(divs):
                    a=a+1

                    try :
                        href = div.find("a").attrs.get('href').replace("./","/")
                        href = self.base_link + category + href
                        self.list_link.append(href)
                    except:
                        break

                self.parser(self.list_link , crawl_date , category , page)
                del self.list_link[:]


    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:
            self.a = self.a + 1
            print("url : " + url)
            while True:
                try:
                    r = requests.get(url, timeout=50, proxies=self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            if r.status_code == 404:
            	continue
            r.encoding = 'utf-8'
            html = r.text

            soup = BeautifulSoup(html, "html.parser")
            title= soup.find("div", class_="title_box").find_next("h2").get_text()
            article = soup.find("div", class_="text botborder").get_text().split("版权声明")
            article = article[0]
            ndate = soup.find("div", class_="info").get_text().split("时间")
            ndate = ndate[1].split("来")
            ndate = ndate[0]


            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            path_html = "/dataph/requests/news/tibet/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

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
            with open("/dataph/requests/news/tibet/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                outfile.write(str(soup))
            with open("/dataph/requests/news/tibet/batch/json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                outfile.write(str(result))
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(page))
            

Tibet().get_items()
