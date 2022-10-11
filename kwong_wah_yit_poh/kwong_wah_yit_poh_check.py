import hashlib
import json
import requests
from pathlib import Path
from datetime import  date, datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout

import time
import random

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

    def create_folder(self, crawl_date, category):
        Path(self.path +"/html/" + crawl_date + "/" + self.current_time + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path +"/json/" + crawl_date + "/" + self.current_time + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.kwongwah.com.my/"
        self.website = "kwong_wah_yit_poh"
        self.a = 0
        self.random_sleep = [1, 2]
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
        self.path = "/news_cn/requests/news/"+ self.website

    def get_items(self):
        with open(self.path + "/cek_url.json", 'r', encoding='utf_8_sig') as outfile:
            self.list_url= json.load(outfile)
        categorys = ['Northern Malaysia', 'Domestic', 'Entertainment', 'International', 'Sport', 'Opinion', 'Finance']
        today_time = datetime.today()
        self.current_time = today_time.strftime("%H")

        for category in categorys:
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)
            if category=='Northern Malaysia':
                url = "https://www.kwongwah.com.my/category/北马新闻/"
                self.get_url(url, category, crawl_date)

            elif category=='Domestic' :
                url = "https://www.kwongwah.com.my/category/国内新闻/"
                self.get_url(url, category, crawl_date)

            elif category=='Entertainment' :
                url = "https://www.kwongwah.com.my/category/娱乐新闻/"
                self.get_url(url, category, crawl_date)

            elif category=='International' :
                url = "https://www.kwongwah.com.my/category/国际新闻/"
                self.get_url(url, category, crawl_date)

            elif category=='Sport' :
                url = "https://www.kwongwah.com.my/category/体育新闻/"
                self.get_url(url, category, crawl_date)

            elif category=='Opinion' :
                url = "https://www.kwongwah.com.my/category/言论/"
                self.get_url(url, category, crawl_date)

            elif category == 'Finance':
                url = "https://www.kwongwah.com.my/category/经济新闻/"
                self.get_url(url, category, crawl_date)




        with open(self.path + "/cek_url.json", 'w', encoding='utf_8_sig') as outfile:
            json.dump(self.list_url, outfile, ensure_ascii=False)



    def get_url (self, url, category, crawl_date):
        for page in range(1,6): #6
            a=True
            while a:
                url21 = url + "page/" + str(page)
                time.sleep(random.choice(self.random_sleep))
                user_agent = random.choice(self.user_agents)
                headers = {
                    'authority': 'www.kwongwah.com.my',
                    'cache-control': 'max-age=0',
                    'upgrade-insecure-requests': '1',
                    'user-agent': user_agent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-US,en;q=0.9,id;q=0.8',

                }
                while True:
                    try:
                        r = requests.get(url21, timeout=20, headers=headers, proxies= self.proxies)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                r.encoding = 'utf-8'
                html=r.text
                soup=BeautifulSoup(html,'html.parser')
                divs=soup.find_all("div", class_='td-block-span6')
                a=0
                if divs:
                    a=False
                else:
                    continue
                for div in divs:
                    try :
                        href = div.find("a").attrs.get('href')
                        self.list_link.append(href)
                    except:
                        continue
                self.parser(crawl_date, category, page)
                self.list_link.clear()
                del self.list_link[:]


    def parser(self, crawl_date, category, page):
        for url in self.list_link:
            if url not in self.list_url:
                self.list_url.append(url)
                try :
                    time.sleep(random.choice(self.random_sleep))
                    print("url : " + url)
                    user_agent = random.choice(self.user_agents)
                    headers = {
                        'authority': 'www.kwongwah.com.my',
                        'cache-control': 'max-age=0',
                        'upgrade-insecure-requests': '1',
                        'user-agent': user_agent,
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'sec-fetch-site': 'none',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-user': '?1',
                        'sec-fetch-dest': 'document',
                        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                    }
                    while True:
                        try:
                            r = requests.get(url, timeout=50, proxies=self.proxies, headers=headers)
                            break
                        except requests.exceptions.RequestException as e:
                            print("connetion timeout")
                            continue
                    r.encoding = 'utf-8'
                    html = r.text
                    soup = BeautifulSoup(html, "html.parser")

                    title= soup.find("h1", class_="entry-title").get_text().replace("\n","")

                    articles = soup.findAll("p")
                    article=""
                    for article21 in articles:
                        article = article + article21.get_text().replace("\n","")

                    ndate = soup.find("time", class_="entry-date updated td-module-date").attrs.get("datetime").split("+")
                    ndate = ndate[0].replace("-","")



                    href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                    path_html = self.path+"/html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html"

                    result = {

                        "title": title,
                        "article": article,
                        "ndate": str(ndate),
                        "category": category,
                        "crawl_date": crawl_date,
                        "path_html": path_html,
                        "url": url

                    }
                    # print (result)
                    # break
                    self.a = self.a + 1
                    with open(self.path+"/html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                        outfile.write(str(soup))
                    with open(self.path+"/json/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".json",'w',encoding='utf_8_sig') as outfile:
                         json.dump(result, outfile, ensure_ascii=False)
                    print("jumlah data: " + str(self.a))
                    print("category : " + category)
                    print("page : " + str(page))
                    self.list_link2.append(url)
                    # break
                except Exception as e :
                    print(e)
                    continue


Kwong().get_items()
