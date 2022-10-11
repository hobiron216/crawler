import hashlib
import json
import random
import socket
import time
import urllib

import requests
from pathlib import Path
import datefinder
from pyvirtualdisplay import Display
from selenium import webdriver

from logger import Logger
from datetime import  date, datetime
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from requests.exceptions import Timeout
from urllib.request import urlopen
from selenium.webdriver import DesiredCapabilities, FirefoxProfile
from selenium.webdriver.firefox.options import Options
import ast
import random
import time



class Huanqiu:
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

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        # self.base_link = "https://china.huanqiu.com/"
        self.a = -1
        self.random_sleep= [1,2]
        self.proxies = {'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
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
        self.path = "/news_cn/requests/news/huanqiu/"
        self.list_link2 = []

    def get_items(self):
        with open(self.path + "/cek_url.json", 'r', encoding='utf_8_sig') as outfile:
            self.list_url= json.load(outfile)
        categorys = ['world', 'china', 'mil', 'taiwan', 'opinion', 'finance', 'tech']
        today_time = datetime.today()
        self.current_time = today_time.strftime("%H")
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        print ("====================================================" + crawl_date + "============================================================")
        list_link = []
        for category in categorys:
            self.z = 0
            self.list_url2 = []

            with open(self.path + "/cek_url_" + category + ".json", 'r', encoding='utf_8_sig') as outfile:
                self.list_url = json.load(outfile)

            # with open(self.path + "/cek_url_" + category + ".json", 'w', encoding='utf_8_sig') as outfile:
            #     json.dump(self.list_url2, outfile, ensure_ascii=False)
            # continue

            a = True
            i = 0
            self.url_break = 0
            while a:
                if self.url_break == 1:
                    break
                today = date.today()
                crawl_date = today.strftime("%Y%m%d")
                self.create_folder(crawl_date, category)
                i = i + 20
                url = "https://" + category + ".huanqiu.com/"
                url_api = "https://" + category + ".huanqiu.com/api/list?node=%22/e3pmh22ph/e3pmh2398%22,%22/e3pmh22ph/e3pmh26vv%22,%22/e3pmh22ph/e3pn6efsl%22,%22/e3pmh22ph/efp8fqe21%22&offset=" + str(i) + "&limit=20"
                if i > 720: #240
                    a = False
                    continue
                c = True
                x = 0
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
                while c:
                    try:
                        api = requests.get(url_api, proxies=self.proxies, timeout=50)
                        c = False
                    except requests.exceptions.RequestException as e:
                        print("connect api timeout")
                        continue
                api = api.text
                #print(api)
                #print(url_api)
                try :
                    api = json.loads(api)
                    aw = api['list'][0]['aid']
                except :
                    continue


                for j in range(0, 20):
                    link = api['list'][j]['aid']
                    list_link.append(link)
                self.parser(url, list_link, crawl_date, category, i)
                del list_link[:]

            if self.list_url2:
                with open(self.path + "/cek_url_" + category + ".json", 'w', encoding='utf_8_sig') as outfile:
                    json.dump(self.list_url2, outfile, ensure_ascii=False)

    def parser(self, url, list_link, crawl_date, category, i):
        for k in list_link:
            url21 = url + "article/" + str(k)
            b = True
            if url21 in self.list_url:
                self.url_break = self.url_break + 1
                break
            self.z = self.z + 1
            if self.z == 1:
                self.list_url2.append(url21)
            time.sleep(random.choice(self.random_sleep))
            print("url : " + url21)

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
            while b:
                try:
                    r = requests.get(url21, proxies=self.proxies, timeout=50, headers=headers)
                    b = False
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue

            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            try :
                title = soup.find("div", class_="t-container-title").get_text()
                article = soup.find("div", class_="l-con clear").get_text()
                ndate = soup.find("p", class_="time").get_text()
            except Exception as e:
                print(e)
                continue
            href21 = hashlib.md5(url21.encode('utf-8')).hexdigest().upper()
            path_html = self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html"

            result = {

                "title": title,
                "article": article,
                "ndate": ndate,
                "category": category,
                "crawl_date": crawl_date,
                "path_html": path_html,
                "url": url21

            }
            self.a = self.a + 1
            with open(self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html",
                      'w', encoding='utf8') as outfile:
                outfile.write(str(soup))
            with open(self.path+"json/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".json",
                      'w', encoding='utf8') as outfile:
                outfile.write(str(result))
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(i))
            self.list_link2.append(url21)

print(Huanqiu().get_items())
