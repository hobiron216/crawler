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
from seleniumwire import webdriver
import random
import time
class Jiemian:

    def create_folder(self, crawl_date, category):
        Path("/dataph/requests/news/jiemian/batch/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path("/dataph/requests/news/jiemian/batch/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def trim_word(self,word, from_start=0, from_end=0):
        return word[from_start:len(word) - from_end]

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "https://www.jiemian.com/lists/"
        self.a = 0
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []
        self.random_sleep = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.display = Display(visible=0, size=(1366, 768))
        self.display.start()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
    def get_browser(self):
        options = {
	        'proxy': {
   		                'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128',
                         'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128',
                         'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
                      }
                   }
        user_agent = random.choice(self.user_agents)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        browser = webdriver.Firefox(seleniumwire_options=options, firefox_profile=profile, executable_path='/usr/local/bin/geckodriver')
        browser.maximize_window()
        return browser

    def get_items(self):
        browser = self.get_browser()
        categorys = ['world', 'china', 'comment', 'financial', 'investment', 'stockmarket' ]
        #32= world , 71=china, 8=comment, 9=financial, 86=investment, 418=stock_market
        for category in categorys:
            if category == 'world' :
                continue
                nid="32"
                self.get_html(category,nid,browser)
            elif category == 'china':

                nid="71"#banyak
                continue
                self.get_html(category, nid,browser)
            elif category == 'comment':

                nid="8"
                self.get_html(category, nid,browser)
            elif category == 'financial' :

                nid="9"#banyak
                self.get_html(category,nid,browser)
            elif category == 'investment':
                nid="86"
                self.get_html(category, nid,browser)
            elif category == 'stockmarket':
                nid="418"
                self.get_html(category, nid,browser)

        browser.close()
        self.display.stop()
    def get_html(self, category, nid, browser):
        url= self.base_link + nid + ".html"
        crawl_date = self.crawl_date()

        self.create_folder(crawl_date, category)
        browser.get(url)
        page="click scroll"
        a=0
        while True:
            try:
                a=a+1
                browser.find_element_by_class_name("load-more").click()
                if nid== '71' or nid=='9' :
                    if a>1000:
                        break
                else:
                    if a>100:
                        break
                # html
                time.sleep(1)
            except:
                break

        html=browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll("div", class_="news-view left card")
        if not divs:
            divs = soup.findAll("div", class_="news-view left")
        for div in divs:
            href=div.find("a").attrs.get("href")
            self.list_link.append(href)
        self.parser(self.list_link,crawl_date,category,page)
        del self.list_link[:]

    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:
            self.a = self.a + 1
            print("url : " + url)
            b = True
            user_agent = random.shuffle(self.user_agents)
            time.sleep(random.choice(self.random_sleep))

            headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.9,id;q=0.8",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'upgrade-insecure-requests': "1",
            'user-agent': user_agent,
            'cookie': 'ncbi_sid=CE899787D9195471_2562SID; pmc.article.report=; _ga=GA1.2.1661002836.1569822027; entrezSort=pmc:; _gid=GA1.2.2059851631.1569998064; WebEnv=1zGUsr%40CE899787D9195471_2562SID; _gat_ncbiSg=1; _gat_dap=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAc+AzPgAwDsAIgJwAstAQtqQIynsccBsLlpRDLgDoAtnACsIADQgArgDsANgHsAhqnlQAHgBdMoAEyZwIgMbSQRY2DMXaxncvMzJWAPTIAzp9lRPbogNWciI3Cy5jaFNlCHQZIOM8fEoAQVoDKjpxMgM2Tk58Ay5SWnxxUQkLXOszDBtTDEcGj29ff0Dg0KqjLAB3fqF5UwAjZEHFEUHkRCEAc2UYKupjFiIuCJkiUmNyLnwLIhYVraPNnpByegOrLAAzVUVPKAP7LB0IXwP9rAPlrHJqGxAfsZLRtv9ASwWNRyHYbiBSEIikJTiArlgFCp1JpdHZXCBUeJ4atWBZxK8CdRJC4Ilhti5YXTwkd/iAAL5soA'
            }

            while b:
                try:
                    r = requests.get(url, timeout=50, proxies=self.proxies, headers=headers)
                    b = False
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text

            soup = BeautifulSoup(html, "html.parser")
            title= soup.find("div", class_="article-header")#.get_text()
            if title == None :
            	continue
            else :
            	title=title.get_text()
            article = soup.find("div", class_="article-main")#.get_text()
            if article == None :
            	continue
            else :
            	article=article.get_text()
            ndate = soup.find("span", class_="author")  # .find_next("span")#.get_text()
            if ndate == None:
                ndate = soup.find("div", class_="article-info").find_next("span").get_text()
            else:
                ndate = ndate.find_next("span").get_text()

            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            path_html = "/dataph/requests/news/jiemian/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

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
            with open("/dataph/requests/news/jiemian/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                outfile.write(str(soup))
            with open("/dataph/requests/news/jiemian/batch/json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                outfile.write(str(result))
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(page))



Jiemian().get_items()

