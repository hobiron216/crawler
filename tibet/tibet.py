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
class Tibet:
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
        Path(self.path+"html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://tibet.cn/cn/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5,6,7,8,9,10]
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
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
        self.path = "/news_cn/requests/news/tibet/"

    def get_items(self):
        categorys = ['politics', 'bwsp', 'aid_tibet', 'religion', 'fp']
        crawl_date = self.crawl_date()
        print ("====================================================" + crawl_date + "============================================================")
        for category in categorys:
            page=-1

            while True:
                crawl_date = self.crawl_date()
                self.create_folder(crawl_date,category)
                page = page + 1
                if page > 6: #6
                    break
                if page==0:
                    url = self.base_link + category
                else:
                    url = self.base_link + category + "/index_" + str(page) + ".html"
                
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

        message = "Engine : Tibet  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))

        with open(self.path + "/cek_url.json", 'w', encoding='utf_8_sig') as outfile:
            json.dump(self.list_link2, outfile, ensure_ascii=False)

    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:
            while True:
                try:
                    print("url : " + url)
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
                            r = requests.get(url, timeout=10,  headers=headers)
                            break
                        except requests.exceptions.RequestException as e:
                            print("connetion timeout")
                            continue
                    if r.status_code == 404:
                        break
                    r.encoding = 'utf-8'
                    html = r.text


                    soup = BeautifulSoup(html, "html.parser")
                    # title= soup.find("title").get_text()
                    title = soup.find("div", class_="title_box").find_next("h2").get_text()
                    article = soup.find("div", class_="text botborder").get_text().split("版权声明")
                    article = article[0]
                    ndate = soup.find("div", class_="info").get_text().split("时间")
                    ndate = ndate[1].split("来")
                    ndate = ndate[0]


                    href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                    path_html = self.path+"html/" + crawl_date + "/" + category + "/" + href21 + ".html"

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
                    with open(self.path+"html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                        outfile.write(str(soup))
                    with open(self.path+"json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                        outfile.write(str(result))
                    print("jumlah data: " + str(self.a))
                    print("category : " + category)
                    print("page : " + str(page))
                    self.list_link2.append(url)
                    break
                except:
                    continue
            

Tibet().get_items()
