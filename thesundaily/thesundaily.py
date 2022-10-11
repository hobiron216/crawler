import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from selenium import webdriver
from pyvirtualdisplay import Display
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
        Path(self.path+"html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.a = 0
        self.z = 0
        self.base_link="https://www.thesundaily.my"
        self.site_name="thesundaily"
        self.random_sleep= [1,2,3,4,5,6,7,8,9,10]
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
        self.list_link = []
        self.path = "/home/news/thesundaily/"
        self.except_json = []

    def get_items(self):
        categorys= ['local', 'world', 'business', 'opinion', 'gear up!', 'supplement']
        for category in categorys:
            if category == 'local':
                url = "https://www.thesundaily.my/search-result/-/search/a/false/true/20210201/20210302/date/true/true/c2VjdGlvbk5hbWU6MMKnYjEzZDc3ZGUtMGMzZC00ZTRmLTk3MzktMDY1Nzg2YmVjY2M0wqdMb2NhbA%3D%3D/0/meta/0/0/0/"
                page=124
                self.get_url(category,url,page)
                break
            elif category == 'world' :
                url = "https://www.thesundaily.my/search-result/-/search/a/false/true/20210201/20210302/date/true/true/c2VjdGlvbk5hbWU6MMKnNmQyNTA2NGYtOTg0Zi00MzcxLWEyMzItNWE0ODljNDVhZDY0wqdXb3JsZA%3D%3D/0/meta/0/0/0/"
                page = 2708
                self.get_url(category, url, page)
            elif category == 'business' :
                url = "https://www.thesundaily.my/search-result/-/search/a/false/true/20210201/20210302/date/true/true/c2VjdGlvbk5hbWU6MMKnOTk0ZjYxMzMtMGY4Yy00MjA2LTlkNTAtODJjYzY5YzllMDAxwqdCdXNpbmVzcw%3D%3D/0/meta/0/0/0/"
                page = 37
                self.get_url(category, url, page)
            elif category == 'sport' :
                url = "https://www.thesundaily.my/search-result/-/search/a/false/true/20210201/20210302/date/true/true/c2VjdGlvbk5hbWU6MMKnZTc3MGU3ZTQtY2I0Zi00ZTUxLWFlZDYtZjBjOTViZGU2OWMxwqdTcG9ydA%3D%3D/0/meta/0/0/0/"
                page = 28
                self.get_url(category, url, page)
            elif category == 'opinion' :
                url = "https://www.thesundaily.my/search-result/-/search/a/false/true/20210201/20210302/date/true/true/c2VjdGlvbk5hbWU6MMKnMThkYzgwZGUtYWVkZi00YmRkLTg0OTYtOThhZTE4MzNiNmExwqdPcGluaW9u/0/meta/0/0/0/"
                page = 6
                self.get_url(category, url, page)
            elif category == 'gear up!' :
                url = "https://www.thesundaily.my/search-result/-/search/a/false/true/20210201/20210302/date/true/true/c2VjdGlvbk5hbWU6MMKnYjUzZTU1ZGUtMDBjMS00NDIwLWExMjMtYjgwOWFhNGVhOGIzwqdHZWFyIHVwIQ%3D%3D/0/meta/0/0/0/"
                page = 1
                self.get_url(category, url, page)
            elif category == 'supplement' :
                url = "https://www.thesundaily.my/search-result/-/search/a/false/true/20210201/20210302/date/true/true/c2VjdGlvbk5hbWU6MMKnZTA4ZTU0MzgtYzM4My00ZmNhLTllYzMtOGM0MDkzNDNjOWQ2wqdTdXBwbGVtZW50/0/meta/0/0/0/"
                page = 1
                self.get_url(category, url, page)

        message = "Engine : thesundaily1  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))
        with open("except.json",'w',encoding='utf_8_sig') as outfile:
            json.dump(self.except_json, outfile, ensure_ascii=False)

    def get_url(self, category, url, page) :
        for i in range(1, (page+1)):
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)
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

            url21 = url + str(i)
            print(url21)
            while True:
                try:
                    r = requests.get(url21, timeout=10, headers=headers, proxies=self.proxies )
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.findAll("li", class_="element")


            for div in divs:
                link = div.find("a").attrs.get("href")
                self.list_link.append(link)
            print(len(self.list_link))
            self.parser(self.list_link, crawl_date, category, i)
            del self.list_link[:]


        
    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:

            url = self.base_link  + url
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
                    r = requests.get(url, timeout=20, proxies=self.proxies, headers=headers)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text

            soup = BeautifulSoup(html, "html.parser")
            title = soup.find("meta", property="og:title")['content']
            ndate = soup.find("div", class_="datefrom small").get_text().split('/')
            ndate = ndate[0]
            ndate= parse(ndate)
            ndate= ndate.strftime('%Y%m%d')
            contents= soup.find("div", class_="paragraph").findAll("p")
            content2=""
            for content21 in contents:
                content2 = content2 + content21.get_text()

            if ". ―" in content2:
                content2 = content2.split(". ―")
                content = content2[0] + "."
                author = content2[1].strip()
            elif ". —" in content2 :
                content2 = content2.split(". —")
                content = content2[0] + "."
                author = content2[1].strip()
            elif ". -" in content2  :
                content2 = content2.split(". -")
                content = content2[0] + "."
                author = content2[1].strip()
            elif '.-' in content2:
                content2 = content2.split('.-')
                content = content2[0] + "."
                author = content2[1].strip()
            elif ".—" in content2 :
                content2 = content2.split(".—")
                content = content2[0] + "."
                author = content2[1].strip()
            elif ".―" in content2:
                content2 = content2.split(".―")
                content = content2[0] + "."
                author = content2[1].strip()

            elif '" -' in content2 :
                # print(content2)
                content2 = content2.split('" -')
                content = content2[0]
                author = content2[1].strip()
            elif '" —' in content2 :
                content2 = content2.split('" —')
                content = content2[0]
                author = content2[1].strip()
            elif '" ―' in content2:
                content2 = content2.split('" ―')
                content = content2[0]
                author = content2[1].strip()
            else :
                try :
                    content=content2
                    author = soup.find("div", class_="byline font-1 small bold").get_text().replace("/","").strip()
                except:
                    self.z= self.z + 1
                    print("z :"+ str(self.z))
                    self.except_json.append(url)
                    author = ""
                    # continue

            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            path_html = self.path + "html/" + crawl_date + "/" + category + "/" + href21 + ".html"

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
            with open(self.path+"html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                    outfile.write(str(soup))
            with open(self.path+"json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf_8_sig') as outfile:
                    json.dump(result, outfile, ensure_ascii=False)
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(page))
            print("gagal " + str(self.z))
            

BjNews().get_items()

