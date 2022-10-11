import hashlib
import json
import requests
from pathlib import Path

from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import random
import time
from dateutil.parser import parse
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
        Path(self.path+"html/" + crawl_date + "/" + category + "/" ).mkdir(parents=True,exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + category + "/" ).mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.bharian.com.my/"
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
        self.path = "/home/news/says/"
        self.site_name = "says"


    def get_items(self):

        categorys= ['news', 'makan', 'fun', 'lifestyle', 'tech', 'seismik', 'entertainment', 'imho', 'sports', 'covid-19', 'travel']

        for category in categorys:
            self.z=0
            if category == 'news':
                continue
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'makan':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'fun':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'lifestyle':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'tech':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'seismik':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'entertainment':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'imho':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'sports':
                url = "https://says.com/my/" + category
                self.get_link(category, url)
            elif category == 'covid-19':
                url = "https://says.com/my/stories/tagged/travel"
                self.get_link(category, url)
            elif category == 'travel':
                url = "https://says.com/my/stories/tagged/COVID19"
                self.get_link(category, url)


    def get_link(self, category,url21):
        for page in range (0,100) :
            if self.z>0:
                break
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)
            link21 = url21 + "?page=" + str(page)
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
                    r = requests.get(link21, timeout=5, headers=headers)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.findAll("li", class_="d-md-flex")
            for div in divs:
                # print("wkwkw")
                link = div.find("a").attrs.get("href")
                self.list_link.append(link)


            self.parser(self.list_link, crawl_date, category, page)
            del self.list_link[:]

    def parser(self, list_link, crawl_date, category, page):

        for url in list_link:
            if self.z>0:
                break
            try :
                url = "https://says.com/" + url
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
                        r = requests.get(url, timeout=5,  headers=headers)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                r.encoding = 'utf-8'
                html = r.text

                soup = BeautifulSoup(html, "html.parser")
                ndate = soup.find("meta", property="article:published_time")['content']
                ndate = ndate.split("T")
                ndate = ndate[0]


                ndate_cek = ndate.split("-")
                ndate = ndate.replace("-", "")
                print(ndate_cek)
                bulan = ndate_cek[1]
                bulan = int(bulan)
                hari = ndate_cek[2]
                hari = int(hari)
                tahun = ndate_cek[0]
                tahun = int(tahun)

                if bulan < 3:
                    self.z = self.z + 1
                    break
                if tahun != 2021:
                    self.z = self.z + 1
                    break
                if bulan == 3 or bulan == 4 or bulan == 5:


                    title = soup.find("meta", property="og:title")['content']
                    try:
                        author = soup.find("div", class_="story-meta").find("a").get_text()
                    except:
                        author = ""

                    ndate = soup.find("meta", property="article:published_time")['content']
                    ndate = ndate.split("T")
                    ndate = ndate[0]
                    ndate = ndate.replace("-", "")
                    contents = soup.find("div", class_="segments-wrap").findAll("p")
                    content22 = ""
                    for content21 in contents:
                        if "Subscribe to our Telegram" in content21.get_text():
                            continue
                        # if "Check out the latest" in content21:
                        #     continue
                        content22 = content22 + content21.get_text().strip()

                    location21 = content22.split(": ")

                    location = location21[0].strip()
                    if "Ayisy Yusof" in location:
                        location = location.replace("Ayisy Yusof", "")
                    try:
                        content = location21[1].strip()
                    except:
                        location = ""

                        content = location21[0].strip()

                    if len(location) > 100:
                        location = ""
                        content = content22



                    href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                    path_html = self.path + "html/" + crawl_date + "/" + category + "/"  + href21 + ".html"

                    result = {

                        "title": title,
                        "ndate": ndate,
                        "category": category,
                        "location" : location,
                        "content" : content,
                        "author" : author,
                        "sitename": self.site_name,
                        "date_crawl": crawl_date,
                        "path_html": path_html,
                        "url": url

                    }
                    # print (result)
                    self.a = self.a + 1
                    with open(self.path+"html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                            outfile.write(str(soup))
                    with open(self.path+"json/" + crawl_date + "/" + category + "/" +  href21 + ".json",'w',encoding='utf_8_sig') as outfile:
                            json.dump(result, outfile, ensure_ascii=False)
                    print("jumlah data: " + str(self.a))
                    print("page : " + str(page))
            except:
                continue



                
        # message = "Engine : Bj News  \n" + "Data : " + str(self.a)
        # self.telegram_bot_sendtext(str(message))
        



BjNews().get_items()

