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
import random
import time
from datetime import  date, datetime
class BjNews:

    def telegram_bot_sendtext(self,bot_message):
        global response
        bot_token = '1381123927:AAEQ169ZfG5qQMvPaNaFyt8zBJzyeZ-feXc'
        bot_chatID = '1008898421'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        while True:
            try:
                response = requests.get(send_text,timeout=10)
                break
            except requests.exceptions.RequestException as e:
                print("gagal kirim telegram")
                continue

        return response.json()
    def create_folder(self, crawl_date, category):
        Path(self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + self.current_time + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://bjnews.com.cn/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5,6,7,8,9,10]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        #self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        self.list_link = []
        self.list_link2 = []
        self.path = "/news_cn/requests/news/bjnews/"

    def get_items(self):
        with open(self.path + "/cek_url.json", 'r', encoding='utf_8_sig') as outfile:
            self.list_url = json.load(outfile)
        categorys = ['Insight','Current', 'Beijing', 'Opinion', 'Finance', 'Technology']
        today_time = datetime.today()
        self.current_time = today_time.strftime("%H")
        crawl_date = self.crawl_date()
        print ("====================================================" + crawl_date + "============================================================")
        for category in categorys:
            page=0
            self.z = 0
            self.list_url2 = []
            self.url_break = 0

            with open(self.path + "/cek_url_" + category + ".json", 'r', encoding='utf_8_sig') as outfile:
                self.list_url = json.load(outfile)
            #
            # with open(self.path + "/cek_url_" + category + ".json", 'w', encoding='utf_8_sig') as outfile:
            #     json.dump(self.list_url2, outfile, ensure_ascii=False)
            # continue
            while True:
                if self.url_break == 1:
                    break

                crawl_date = self.crawl_date()
                self.create_folder(crawl_date,category)
                if category == 'Insight':
                	category21='depth'
                elif category == 'Current':
                	category21='news'
                elif category== 'Beijing' :
                	category21= 'beijing'
                elif category == 'Opinion' :
                	category21 = 'point'
                elif category== 'Finance' :
                	category21 = 'financial'
                elif category== 'Technology' :
                	category21 = 'technology'
                page = page + 1
                if page > 15 : #5
                    break
                url = self.base_link + category21 + "/" + str(page) + ".html"
                time.sleep(random.choice(self.random_sleep))
                
                user_agent = random.choice(self.user_agents)
                
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
                while True:
                    try:
                        r = requests.get(url, timeout=50, proxies=self.proxies, headers=headers)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                html=r.text
                soup=BeautifulSoup(html,'html.parser')
                divs=soup.find_all("div", class_="pin_demo")
               
                if "没有找到数据" in html:
                    break

                a=0
                for i,div in enumerate(divs):
                    a=a+1
                    try :
                        href = div.find("a").attrs.get('href')
                        self.list_link.append(href)
                    except:
                        break
                self.parser(self.list_link , crawl_date , category , page)
                del self.list_link[:]
                if self.list_url2:
                    with open(self.path + "/cek_url_" + category + ".json", 'w', encoding='utf_8_sig') as outfile:
                        json.dump(self.list_url2, outfile, ensure_ascii=False)


        
    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:
            if url in self.list_url:
                self.url_break = self.url_break + 1
                break
            self.z = self.z + 1
            if self.z == 1:
                self.list_url2.append(url)
            self.list_url.append(url)
            time.sleep(random.choice(self.random_sleep))
            print("url : " + url)
            user_agent = random.choice(self.user_agents)
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
            while True:
                try:
                    r = requests.get(url, timeout=50, proxies=self.proxies, headers=headers, params={'q':'goog'})
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text

            soup = BeautifulSoup(html, "html.parser")
            title= soup.find("div", class_="bread-line")#.find_next("h1").get_text()
            if title == None :
                continue
            else :
                title = title.find_next("h1").get_text()
            article = soup.find("div", class_="article-text")#.get_text()
            if article == None :
                continue
            else :
                article=article.get_text()
            ndate = soup.find("span", class_="timer").get_text()

            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            path_html = self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html"

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
            self.a = self.a + 1
            with open(self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                outfile.write(str(soup))
            with open(self.path+"json/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                outfile.write(str(result))
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(page))
            self.list_link2.append(url)


BjNews().get_items()

