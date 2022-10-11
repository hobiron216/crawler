import hashlib
import json
import requests
from pathlib import Path
from logger import Logger
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout

class News_Cn:

    def create_folder(self, crawl_date, category):
        Path("/dataph/requests/news/news_cn/batch2/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path("/dataph/requests/news/news_cn/batch2/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def trim_word(self,word, from_start=0, from_end=0):
        return word[from_start:len(word) - from_end]

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://news.cn/"
        self.a = 0
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []

    def get_items(self):
        categorys = ['politics', 'local', 'legal', 'mil', 'fortune', 'money']
        for category in categorys:
            if category == 'politics' :
                #continue
                nid="113352"
                self.get_html(category,nid)
            elif category == 'local':
                #continue
                nid="113321"
                self.get_html(category, nid)
            elif category == 'legal':
                #continue
                nid="113207"
                self.get_html(category, nid)
            elif category == 'mil':
                continue
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
                            continue
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
                        self.get_html(category, url)
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


    def get_html(self,category,nid):
        page=0
        while True:
            page=page+1
            if nid=="11139631" and category == "mil":
                if page<=91 : #daily
                    continue
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)
            while True:
                try:
                    r=requests.get("http://qc.wa.news.cn/nodeart/list?nid="+nid+"&pgnum="+str(page)+"&cnt=10&tp=1&orderby=1?callback=jQuery11240581078843432933_1603256936706&_=1603256936707", timeout=50,  proxies=self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion api timeout")
                    continue

            r=r.text
            if len(r)<=76:
                break
            
            if "DTD HTML 4.01 Transitional//EN" in r:
                continue

            r=self.trim_word(r,41,1)
            
            #print(r)
            # r=r.split("(")
            # r=r[1].split(")")
            # r=r[0]
            #try:
            r= json.loads(r)
            r=r['data']['list']
            # except Exception as e:
            #     print("awwww")
            #     r=r+ '"'+ "}]}}"
            #     r = json.dumps(r)
            #     r=ast.literal_eval(r)
            #     r= json.loads(r)
            #     print(r)
            for j in r:
                link=j['LinkUrl']
                self.list_link.append(link)
            self.parser(self.list_link,crawl_date,category,page,nid)
            del self.list_link[:]

    def parser(self,list_link, crawl_date, category, page,nid):

        for url in list_link:
            try:
                self.a = self.a + 1
                b = True
                if len(url)<55:
                    continue
                while b:
                    try:
                        r = requests.get(url, timeout=50, proxies=self.proxies)
                        b = False
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                r.encoding = 'utf-8'
                html = r.text
                #print(html)
                soup = BeautifulSoup(html, "html.parser")
                title = soup.find("div", class_="h-title")#.get_text()
                if title == None:
                    title=soup.find("h1", id="title")
                    if title==None:
                        continue
                    else:
                        title=title.get_text()
                        article=soup.find("div", id="article").get_text()
                        article=article.split("字小")
                        article=article[1]
                        ndate = soup.find("span", class_="time").get_text()

                else:
                    title=title.get_text()
                    article = soup.find("div", class_="p-right left").get_text()
                    ndate = soup.find("span", class_="h-time").get_text()

                href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                path_html = "/dataph/requests/news/news_cn/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

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
                with open("/dataph/requests/news/news_cn/batch2/html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                       outfile.write(str(soup))
                with open("/dataph/requests/news/news_cn/batch2/json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                       outfile.write(str(result))
                     
                print("jumlah data: " + str(self.a))
                print("category : " + category)
                print("page : " + str(page))
                print("nid :" + str(nid))
                print("url :" + url)
            except:
                pass



    def get_html_soup(self,category,url):
        crawl_date=self.crawl_date()
        nid=0
        self.create_folder(crawl_date, category)
        page = "scroll"
        while True:
                try:
                    r = requests.get(url, timeout=50, proxies=self.proxies)
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
            # if a>40: #daily
            #     break
            href = div.find("a").attrs.get('href')
            self.list_link.append(href)

        self.parser(self.list_link,crawl_date,category,page,nid)
        del self.list_link[:]

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date


News_Cn().get_items()

