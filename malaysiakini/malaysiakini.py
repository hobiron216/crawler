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
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import urllib.request as request21
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
        Path(self.path+ self.site_name + "/html/" + crawl_date + "/" + category + "/" ).mkdir(parents=True,exist_ok=True)
        Path(self.path+ self.site_name + "/json/" + crawl_date + "/" + category + "/" ).mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://m.malaysiakini.com/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5,6,7,8,9,10]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        #self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11 _5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
        self.path = "/home/news/"
        self.site_name = "malaysiakini"

    def get_items(self):
        categorys=['terkini', 'parlimen', 'sukan', 'seni & hiburan', 'global', 'pilihan editor', 'kolum']
        for category in categorys:
            if category == 'terkini' :
                url = "https://m.malaysiakini.com/api/my/latest/news/"
                tag = "news/"
                self.get_link(category, url, tag)
            elif category == 'parlimen' :
                url = "https://m.malaysiakini.com/api/my/tag/parlimen/"
                tag = "news/"
                self.get_link(category, url, tag)
            elif category == 'sukan' :
                url = "https://m.malaysiakini.com/api/my/latest/sukan/"
                tag = "sukan/"
                self.get_link(category, url, tag)
            elif category == 'seni & hiburan' :
                url = "https://m.malaysiakini.com/api/my/latest/hiburan/"
                tag = "hiburan/"
                self.get_link(category, url, tag)
            elif category == 'global' :
                url = "https://m.malaysiakini.com/api/my/tag/global/"
                tag = "news/"
                self.get_link(category, url, tag)
            elif category == 'pilihan editor' :
                url = "https://m.malaysiakini.com/api/my/tag/pilihan%20editor/"
                tag = "news/"
                self.get_link(category, url, tag)
            elif category == 'kolum' :
                url = "https://m.malaysiakini.com/api/my/latest/columns/"
                tag = "columns/"
                self.get_link(category, url, tag)




    def get_link(self, category, url21, tag):
        z=0
        for page in range (0,101) :
            if z>0:
                break
            link21 = url21 + str(page) + "?captcha_hash=0d49e1d2e2029cf6fb159a3153b3a1d5"
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
                    r = requests.get(link21, timeout=10, proxies=self.proxies, headers=headers)
                    r.encoding = 'utf-8'
                    try:
                        r = json.loads(r.text)
                    except:
                        continue
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue


            for data_json in r['stories']:

                sid = data_json['sid']
                url = self.base_link + tag + str(sid)
                title = data_json['title']

                print("url : " + url)
                ndate = data_json['date_pubh']
                ndate = ndate.split(" ")
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

                if bulan < 2:
                    z = z + 1
                    break
                if tahun != 2021:
                    z = z + 1
                    break

                if bulan == 3 or bulan == 2:

                    if hari > 2:

                        if bulan > 2:
                            print("skip")
                            continue


                    user_agent = random.choice(self.user_agents)

                    while True:
                        try:
                            proxy_handler = request21.ProxyHandler(self.proxies)
                            opener = request21.build_opener(proxy_handler)
                            r = opener.open(Request(url,  headers={'User-Agent': user_agent} ) ).read()
                            break
                        except HTTPError as e:
                            print("connetion timeout")
                            continue
                        except URLError as e:
                            print("connetion timeout")
                            continue
                    html = r
                    # print(html)

                    soup = BeautifulSoup(html, "html.parser")
                    try:
                        author = soup.find("meta", property="article:author")['content']
                    except:
                        author = ""


                    contents = soup.find("div",id="content").findAll("p")
                    content = ""
                    for content21 in contents:
                        content = content + content21.get_text().replace("[Baca berita penuh]","").strip()

                    crawl_date = self.crawl_date()
                    self.create_folder(crawl_date, category)

                    href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                    path_html = self.path + self.site_name + "/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

                    result = {

                        "title": title,
                        "ndate": ndate,
                        "category": category,
                        "content" : content,
                        "author" : author,
                        "sitename": self.site_name,
                        "date_crawl": crawl_date,
                        "path_html": path_html,
                        "url": url

                    }
                    # print (result)
                    self.a = self.a + 1
                    with open(self.path + self.site_name + "/html/" + crawl_date + "/" + category +  "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                            outfile.write(str(soup))
                    with open(self.path + self.site_name + "/json/" + crawl_date + "/" + category + "/" +  href21 + ".json",'w',encoding='utf_8_sig') as outfile:
                            json.dump(result, outfile, ensure_ascii=False)
                    print("jumlah data: " + str(self.a))
                    print("sub_category : " + category)
                    print("page : " + str(page))



                
        # message = "Engine : Bj News  \n" + "Data : " + str(self.a)
        # self.telegram_bot_sendtext(str(message))
        



BjNews().get_items()
