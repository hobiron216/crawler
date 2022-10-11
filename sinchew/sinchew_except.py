import hashlib
import time

import requests
from pathlib import Path
import datefinder
from pyvirtualdisplay import Display
from selenium import webdriver


from datetime import  date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from seleniumwire import webdriver
import random
import multiprocessing
import json

class Sinchew:
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
        
    def create_folder(self,crawl_date,type):
        # Path("/home/shahid/Documents/requests/news/sinchew/html/"+ crawl_date+ "/world/").mkdir(parents=True, exist_ok=True)
        # Path("/home/shahid/Documents/requests/news/sinchew/json/" + crawl_date + "/world/").mkdir(parents=True, exist_ok=True)
        Path(self.path+"html/"+ crawl_date+ "/" + type + "/").mkdir(parents=True, exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + type + "/").mkdir(parents=True, exist_ok=True)
        # "/dataph/requests/news/sinchew/html/" + crawl_date + "/world/" + href21 + ".html"

    def __init__(self):
        self.base_link = "https://www.sinchew.com.my/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5]
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        #self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
        self.path="/news_cn/requests/news/sinchew/"
        self.href=[]


    def get_items(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        type='except'

        with open('/home/crawler/berita_cina/sinchew/except/'+ crawl_date+'/'+ 'except.json', 'r') as outfile21:
            aw = json.load(outfile21)
            for link in aw:
                # aw21=aw21.replace("'","").replace("[","").replace("]","")
                self.href.append(link)
        print(self.href)
                # self.get_parser(type, self.href, crawl_date)

        # print(self.link_fail)
        # message = "Engine : Sinchew  \n" + "Data : " + str(self.a)
        # self.telegram_bot_sendtext(str(message))

        return type

    def get_parser(self,type,link, crawl_date ):
        # i=0
        for href in link :
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
            time.sleep(random.choice(self.random_sleep))
            valid = False
            while not valid:
                try:
                    #time.sleep(2)
                    r=requests.get(href,timeout=10,headers=headers, proxies=self.proxies)
                    valid=True
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue
            print("url : " + href)
            html=r.text

            # if html=="b' '":
            #     continue
            if html:
                soup=BeautifulSoup(html,"html.parser")
                time21=soup.find("div", attrs={"style":"width:670px;text-align:left;float:left;margin-top:10px;border-right: 1px solid #ccc;"})
                if time21==None:
                    print("time salah ke-1")
                    self.link_fail.append(href)
                    # if self.test==1:
                    #     print(str(soup))
                    continue
                else :
                    time21=time21.get_text().split(" ")
                    match = datefinder.find_dates(time21[0])


                for ndate in match:
                    title=soup.find("h1", attrs={"style":"color:black;font-size:34px;"})
                    if title==None:
                        title= soup.find("div", attrs={"style":"color:black;font-size:34px;"}).get_text()
                    else :
                        title= title.get_text()
                    # headlines= soup.find("div", attrs={"style":"color:#cd2026;font-size:16px"}).get_text()
                    category=soup.find("div", class_="neiwen-top-title").get_text().replace("\n","")
                    article=soup.find("div", id="dirnum").get_text()

                    href21= hashlib.md5(href.encode('utf-8')).hexdigest().upper()
                    path_html = self.path+"html/"+crawl_date+ "/" +type + "/" + href21 + ".html"

                    ndate=ndate.strftime("%Y-%m-%d %H:%M:%S")


                    result = {

                                    "title": title,
                                    "article": article,
                                    "ndate": ndate,
                                    "category": category,
                                    "crawl_date" : crawl_date,
                                    "path_html" : path_html,
                                    "url"       : href


                                }
                    self.a = self.a + 1

                    #print(result)
                    print("jumlah data : " + str(self.a))
                    print("type : " + type)
                    print("page : " + str(i))
                    if type== 'mykampung' :
                        print("node : " + city)
                    else :
                        print("node : " + link)


                    # print(obj)
                    self.create_folder(crawl_date, type)
                    with open(self.path+"html/" + crawl_date + "/" +type + "/" + href21 +'.html', 'w',encoding='utf8') as outfile:
                         outfile.write(str(soup))
                    with open(self.path+"json/" + crawl_date + "/" +type + "/" + href21+'.json', 'w', encoding='utf8') as outfile:
                         outfile.write(str(result))
                    # with open('cina.json', 'w') as outfile:
                    #     outfile.write(str(result))
        return self.a


    def quit_browser(self):
        try:
            if self.browser:
                self.browser.quit()
                self.display.stop()
                self.logger.log('quit browser ...')
        except:
            raise


multiprocessing.Process(target=Sinchew().get_items())
#print(Sinchew().get_items())
