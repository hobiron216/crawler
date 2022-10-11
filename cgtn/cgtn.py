import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
# import cloudscraper
import datetime as datetime21
import time
import random
from datetime import datetime

# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)
class Kwong:

    def telegram_bot_sendtext(self,bot_message):
        global response
        bot_token = '1381123927:AAEQ169ZfG5qQMvPaNaFyt8zBJzyeZ-feXc'
        bot_chatID = '1008898421'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        while True:
            try:
                response = requests.get(send_text, timeout=10)
                break
            except requests.exceptions.RequestException as e:
                print("gagal kirim telegram")
                continue

        return response.json()

    def create_folder(self, crawl_date, category, sub_category):
        Path(self.path +"/html/" + crawl_date + "/" + category + "/" + sub_category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path +"/json/" + crawl_date + "/" + category + "/" + sub_category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.cgtn.com/"
        self.website = "cgtn"
        self.a = 0
        self.random_sleep = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
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
        self.path = "/news_cn/requests/news/"+ self.website + "/new_daily"
        # self.scraper = cloudscraper.create_scraper()

    def get_items(self):
        categorys = ['china', 'world', 'politics', 'business', 'tech-sci', 'culture', 'opinions', 'europe' ]

        for category in categorys:
            crawl_date = self.crawl_date()
            # crawl_date = "20211003"

            if category=='china':

                sub_categorys = ['china']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)

            elif category=='world' :
                sub_categorys = ['world']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)

            elif category=='politics' :
                sub_categorys = ['diplomacy', 'leadership', 'politics', 'world']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)

            elif category=='business' :
                sub_categorys = ['business', 'company', 'economy', 'in-depth', 'markets']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)

            elif category=='tech-sci'   :
                sub_categorys = ['tech-sci']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)

            elif category == 'culture':
                sub_categorys = ['culture']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)

            elif category == 'opinions':
                sub_categorys = ['opinions']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)

            elif category == 'europe':
                sub_categorys = ['europe']
                for sub_category in sub_categorys:
                    self.get_url(sub_category, category, crawl_date)



            # break
        message = "Engine : " + self.website + "\n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))
        with open(self.path + "/cek_url.json", 'w', encoding='utf_8_sig') as outfile:
            json.dump(self.list_link2, outfile, ensure_ascii=False)



    def get_url (self, sub_category, category, crawl_date):

        if category == sub_category:
            url21 = self.base_link + category
        else:
            url21 =  self.base_link + category + "/" + sub_category + ".html"
        time.sleep(random.choice(self.random_sleep))
        user_agent = random.choice(self.user_agents)
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',

        }

        print(url21)
        while True:
            try:
                r = requests.get(url21, headers=headers, timeout=10)
                break
            except requests.exceptions.RequestException as e:
                print("connetion timeout")
                continue
        html=r.text

        soup=BeautifulSoup(html,'html.parser')
        divs=soup.find("body").findAll("a")
        a=0
        # print(html)
        today = date.today() - datetime21.timedelta(1)
        crawl_date_news = today.strftime("%Y-%m-%d")
        # crawl_date_news = today.strftime("2021-10-30")
        for div in divs:

            href = div.attrs.get('href')
            if "/news/" in str(href):
                if crawl_date_news in str(href) :
                    # print(href)
                    self.list_link.append(href)

        # print(len(self.list_link))

        self.parser(crawl_date, category, sub_category)
        self.list_link.clear()
        del self.list_link[:]


    def parser(self, crawl_date, category,  sub_category):
        for url in self.list_link:
            try :
                self.create_folder(crawl_date, category, sub_category)
                time.sleep(random.choice(self.random_sleep))
                print("url : " + url)
                user_agent = random.choice(self.user_agents)
                headers = {
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0',
                    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                    'sec-ch-ua-mobile': '?0',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
                }
                while True:
                    try:
                        r = requests.get(url, headers=headers, timeout=10)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                r.encoding = 'utf-8'
                html = r.text
                soup = BeautifulSoup(html, "html.parser")

                title= soup.find("div", class_="news-title").get_text().replace("\n","")

                articles = soup.find("div", class_="m-content").findAll("p")
                article=""
                for article21 in articles:
                    article = article + article21.get_text().replace("\n","")

                ndate = soup.find("span", class_="date").get_text().replace("\n","").strip()
                ndate = datetime.strptime(ndate, '%H:%M, %d-%b-%Y')
                sub_category21 = soup.find("span", class_="section").get_text().replace("\n","").strip()
                # ndate = ndate[0].replace("-","")



                href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                path_html = self.path+"/html/" + crawl_date + "/" + category + "/" + sub_category + "/" +   href21 + ".html"

                result = {

                    "title": title,
                    "url": url,
                    "ndate": str(ndate),
                    "crawl_date": crawl_date,
                    "path_html": path_html,
                    "category": category,
                    "sub_category": sub_category21,
                    "article": article,

                }
                # print (result)
                # break
                self.a = self.a + 1
                with open(self.path+"/html/" + crawl_date + "/" + category + "/" + sub_category + "/" +  href21 + ".html",'w',encoding='utf8') as outfile:
                    outfile.write(str(soup))
                with open(self.path+"/json/" + crawl_date + "/" + category + "/" + sub_category + "/" +  href21 + ".json",'w',encoding='utf_8_sig') as outfile:
                    json.dump(result, outfile, ensure_ascii=False)
                print("jumlah data: " + str(self.a))
                print("category : " + category)
                print("sub-category : " + sub_category )
                self.list_link2.append(url)
            except:
                continue
                # break



Kwong().get_items()
