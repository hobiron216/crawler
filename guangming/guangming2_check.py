import hashlib
import json
import requests
from pathlib import Path
from logger import Logger
from datetime import  date, datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from selenium import webdriver
from pyvirtualdisplay import Display
import time
from seleniumwire import webdriver
from urllib.request import urlopen
import socket
import urllib
import random

class Guangming:

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
        self.base_link = ".gmw.cn/"
        self.a = 0
        self.proxies = {  'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []
        self.list_link2 = []

        self.random_sleep = [1, 2]

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        self.path = "/news_cn/requests/news/guangming/"


    def get_items(self):
        with open(self.path + "/cek_url2.json", 'r', encoding='utf_8_sig') as outfile:
            self.list_url= json.load(outfile)
        categorys = ['politics', 'world', 'mil', 'legal', 'economy']
        crawl_date = self.crawl_date()
        today_time = datetime.today()
        self.current_time = today_time.strftime("%H")
        print ("====================================================" + crawl_date + "============================================================")

        for category in categorys:
            if category == 'politics' :
                continue
                nodes =['node_9844', 'node_9840', 'node_103380', 'node_9831', 'node_9828', 'node_9826']
                for node in nodes:
                    self.get_html(category,node)

            elif category == 'world' :
                continue

                nodes =['node_4661', 'node_24177', 'node_4485', 'node_4696', 'node_24179', 'node_4660']
                for node in nodes:
                    self.get_html(category,node)

            elif category == 'mil' :
                nodes =['node_8986', 'node_8981', 'node_8984', 'node_8982', 'node_11177', 'node_11178', 'node_11176', 'node_8978', 'node_8979']
                for node in nodes:
                    self.get_html(category,node)

            elif category == 'legal' :
                nodes =['node_9020', 'node_9017', 'node_12581', 'node_9018', 'node_5452', 'node_12328', 'node_9015']
                for node in nodes:
                    self.get_html(category,node)
            elif category == 'economy' :
                continue
                nodes =['node_59269', 'node_8971', 'node_21787', 'node_9141']
                for node in nodes:
                    self.get_html(category,node)

        with open(self.path + "/cek_url2.json", 'w', encoding='utf_8_sig') as outfile:
            json.dump(self.list_url, outfile, ensure_ascii=False)
    def get_html(self, category, node):
        a=0
        while True :
            a=a+1
            # if category == 'economy' or node=='node_9826':
            #     if a>10:
            #         break
            # else:
            if a>3:#3
                break
            if a==1 :
                url= "https://" + category + self.base_link + node + ".htm"
            else :
                url = "https://" + category + self.base_link + node + "_" + str(a) + ".htm"

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
            while True:
                try:
                    r = requests.get(url, timeout=10, proxies=self.proxies, headers=headers)
                    break
                except requests.exceptions.RequestException as e:
                    continue
            r.encoding = 'utf-8'
            html = r.text
            if "请检查网址是否正确" in html:
                break
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)

            soup = BeautifulSoup(html, 'html.parser')
            divs = soup.findAll("ul", class_="channel-newsGroup")
            for div in divs:
                divs2=div.findAll("li")
                for div2 in divs2 :
                    href=div2.find("a").attrs.get("href")
                    self.list_link.append(href)
            # print(self.list_link)
            self.parser(self.list_link,crawl_date,category,node)
            del self.list_link[:]

    def parser(self,list_link, crawl_date, category, node):
        for url in list_link:
            if url not in self.list_url:

                if "https" not in url:
                    url = "https://" + category + self.base_link + url
                self.list_url.append(url)
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
                        r = requests.get(url, timeout=10, proxies=self.proxies, headers=headers)
                        b = False
                    except requests.exceptions.RequestException as e:
                        continue
                r.encoding = 'utf-8'
                html = r.text
                #print(html)

                soup = BeautifulSoup(html, "html.parser")
                try :
                    title= soup.find("h1", class_="u-title").get_text()
                    article = soup.find("div", class_="u-mainText").get_text()
                except:
                    continue
                if len(article) <=200:
                    continue
                try:
                    ndate = soup.find("span", class_="m-con-time").get_text()
                except:
                    try:
                        ndate = soup.find("div", class_="m-contentMsg").get_text()
                        ndate = ndate.split("来源")
                        ndate = ndate[0].split(" ")
                        ndate = ndate[4] + " " + ndate[5]
                        # ndate2 = ndate[]
                    except Exception as e:
                        print(e)
                        try:
                            ndate = soup.find("span", class_="u-time").get_text()
                        except:
                            continue



                href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                path_html = self.path+"html/" + crawl_date +  "/" + self.current_time + "/" + category + "/" + href21 + ".html"

                result = {

                    "title": title,
                    "article": article,
                    "ndate": ndate,
                    "category": category,
                    "crawl_date": crawl_date,
                    "path_html": path_html,
                    "url": url

                }
                self.a = self.a + 1
                # print (result)
                with open(self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                    outfile.write(str(soup))
                with open(self.path+"json/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                    outfile.write(str(result))
                print("jumlah data: " + str(self.a))
                print("category : " + category)
                print("page : " + str(node))
                self.list_link2.append(url)


Guangming().get_items()
