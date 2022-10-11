import hashlib
import json
import requests
from pathlib import Path
from logger import Logger
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import random
import time
class News_Cn:
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

    def trim_word(self,word, from_start=0, from_end=0):
        return word[from_start:len(word) - from_end]

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://news.cn/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5,6,7,8,9,10]
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
        self.list_link = []
        self.path = "/news_cn/requests/news/news_cn/"

    def get_items(self):
        categorys = ['politics', 'local', 'legal', 'mil', 'fortune', 'money']
        crawl_date = self.crawl_date()
        print ("====================================================" + crawl_date + "============================================================")
        for category in categorys:
            if category == 'politics' :
                nid="113352"
                self.get_html(category,nid)
            elif category == 'local':
                nid="113321"
                self.get_html(category, nid)
            elif category == 'legal':
                nid="113207"
                self.get_html(category, nid)
            elif category == 'mil':
                for i in range(1,6):
                    if i == 1:
                        nid="11139631"
                        self.get_html(category, nid)
                    elif i == 2:
                        nid="11139635"
                        self.get_html(category, nid)
                    elif i == 3:
                        nid = "11139636"
                        self.get_html(category, nid)
                    elif i == 4:
                        nid = "11139637"
                        self.get_html(category, nid)
                    elif i == 5:
                        nid = "11139638"
                        self.get_html(category, nid)
            elif category == 'fortune':
                   for i in range(1,5):
                        if i == 1:
                            nid="115093"
                            self.get_html(category, nid)
                        elif i == 2:
                            url= "http://www.news.cn/finance/"

                            self.get_html_soup(category, url)
                        elif i == 3:
                            nid = "1151357"
                            self.get_html(category, nid)
                        elif i == 4:
                            nid = "1187294"
                            self.get_html(category, nid)
            elif category == 'money':
                for i in range(1,7):
                    if i == 1:
                        url="http://www.news.cn/money/index.htm"
                        self.get_html_soup(category, url)
                    elif i == 2:
                        nid="11142781"
                        self.get_html(category, nid)
                    elif i == 3:
                        nid = "11142786"
                        self.get_html(category, nid)
                    elif i == 4:
                        nid = "11142787"
                        self.get_html(category, nid)
                    elif i == 4:
                        nid = "11142788"
                        self.get_html(category, nid)
                    elif i == 4:
                        nid = "11142790"
                        self.get_html(category, nid)
        message = "Engine : News Cn  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))

    def get_html(self,category,nid):
        page=0
        print (nid)
        while True:
            page=page+1
            if page>20 : #daily
                break
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)
            time.sleep(random.choice(self.random_sleep))
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
                    r=requests.get("http://qc.wa.news.cn/nodeart/list?nid="+nid+"&pgnum="+str(page)+"&cnt=10&tp=1&orderby=1?callback=jQuery11240581078843432933_1603256936706&_=1603256936707", timeout=50,  proxies=self.proxies, headers = headers)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion api timeout")
                    continue

            r=r.text
            if len(r)<=76:
                break

            r=self.trim_word(r,41,1)
            #print(r)
            # r=r.split("(")
            # r=r[1].split(")")
            # r=r[0]
            #try:
            r= json.loads(r)
            # except Exception as e:
            #     print("awwww")
            #     r=r+ '"'+ "}]}}"
            #     r = json.dumps(r)
            #     r=ast.literal_eval(r)
            #     r= json.loads(r)
            #     print(r)

            for j in range(0,10):
                link=r['data']['list'][j]['LinkUrl']
                self.list_link.append(link)
            self.parser(self.list_link,crawl_date,category,page)
            del self.list_link[:]

    def parser(self,list_link, crawl_date, category, page):

        for url in list_link:
            print("url : " + url)
            b = True
            if len(url)<55:
                continue
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
            try :
                title = soup.find("div", class_="h-title")#.get_text()
                if title == None:
                    continue
                else:
                    title=title.get_text()
                article = soup.find("div", class_="p-right left").get_text()
                ndate = soup.find("span", class_="h-time").get_text()
            except:
                continue

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



    def get_html_soup(self,category,url):
        crawl_date=self.crawl_date()
        self.create_folder(crawl_date, category)
        page = "scroll"
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
                    print("connetion html_soup timeout")
                    continue
        html=r.text
        soup=BeautifulSoup(html,'html.parser')
        divs=soup.find_all("li", class_="clearfix")

        a=0
        for i,div in enumerate(divs):
            a=a+1
            if a==1:
                continue
            if a>24: #daily
                break
            href = div.find("a").attrs.get('href')
            self.list_link.append(href)

        self.parser(self.list_link,crawl_date,category,page)
        del self.list_link[:]

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date


News_Cn().get_items()

