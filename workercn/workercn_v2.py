import hashlib
import json
import requests
from pathlib import Path
from datetime import date
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
        Path(self.path +"/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path +"/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        # crawl_date = today.strftime("20211203")
        return  crawl_date

    def __init__(self):
        self.base_link = "http://www.workercn.cn/"
        self.website = "workercn"
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
        self.path = "/news_cn/requests/news/"+ self.website

    def get_items(self):
        categorys = ['learning', 'politic', 'view', 'headquarter', 'union', 'opinion', 'international', 'daily', 'finance', 'entertaiment', 'military',
                     'rights', 'career', 'theory', 'people', 'column', 'rolling']

        for category in categorys:
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)
            if category=='learning':
                url = "http://www.workercn.cn/json/main/34192"
                self.get_url(url, category, crawl_date)

            elif category=='politic' :
                url = "http://www.workercn.cn/json/sz/34196"
                self.get_url(url, category, crawl_date)

            elif category=='view' :
                url = "http://www.workercn.cn/json/main/34032"
                self.get_url(url, category, crawl_date)

            elif category=='headquarter' :
                url = "http://www.workercn.cn/json/main/34166"
                self.get_url(url, category, crawl_date)

            elif category=='union' :
                url = "http://www.workercn.cn/json/ghgz/34165"
                self.get_url(url, category, crawl_date)

            elif category=='opinion' :
                url = "http://www.workercn.cn/json/pl/34199"
                self.get_url(url, category, crawl_date)

            elif category == 'international':
                url = "http://www.workercn.cn/json/gj/34067"
                self.get_url(url, category, crawl_date)

            elif category == 'daily':
                url = "http://www.workercn.cn/json/sh/34055"
                self.get_url(url, category, crawl_date)
            elif category == 'finance':
                url = "http://www.workercn.cn/json/cj/34179"
                self.get_url(url, category, crawl_date)
            elif category == 'entertaiment':
                url = "http://www.workercn.cn/json/yl/34060"
                self.get_url(url, category, crawl_date)
            elif category == 'military':
                url = "http://www.workercn.cn/json/js/34066"
                self.get_url(url, category, crawl_date)
            elif category == 'rights':
                url = "http://www.workercn.cn/json/wq/34164"
                self.get_url(url, category, crawl_date)
            elif category == 'career':
                url = "http://www.workercn.cn/json/jyycy/34168"
                self.get_url(url, category, crawl_date)
            elif category == 'theory':
                url = "http://www.workercn.cn/json/lilun/34198"
                self.get_url(url, category, crawl_date)
            elif category == 'people':
                url = "http://www.workercn.cn/json/rw/34167"
                self.get_url(url, category, crawl_date)
            elif category == 'column':
                url = "http://www.workercn.cn/json/main/34197"
                self.get_url(url, category, crawl_date)
            elif category == 'rolling':
                url = "http://www.workercn.cn/json/main/28261"
                self.get_url(url, category, crawl_date)
            # break

        message = "Engine : workercn \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))

        # with open(self.path + "/cek_url.json", 'w', encoding='utf_8_sig') as outfile:
        #     json.dump(self.list_link2, outfile, ensure_ascii=False)



    def get_url (self, url, category, crawl_date):
        for page in range(1,6): #6
            url21 = url + "_" + str(page) + ".json"
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
            try:
                api = json.loads(html)
            except:
                continue
            for data in api :
                href = self.base_link + data['href']
                self.list_link.append(href)
            # print(self.list_link)

            self.parser(crawl_date, category, page)
            self.list_link.clear()
            del self.list_link[:]
            # break


    def parser(self, crawl_date, category, page):
        for url in self.list_link:
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
                r.encoding = 'GBK'
                html = r.text
                soup = BeautifulSoup(html, "html.parser")

                # title = soup.find("meta", property="og:title")['content']
                title = soup.find("title").get_text()

                articles = soup.find("div", class_="ccontent").get_text().strip().replace("\n","|")

                # ndate = soup.find("meta", name="publishdate")['content']
                ndate = soup.find("span", class_="time").get_text()
                # ndate = ndate[0].replace("-","")



                href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                path_json = self.path+"/json/" + crawl_date + "/" + category + "/" + href21 + ".json"

                result = {

                    'title': title,
                    'url': url,
                    'ndate': ndate,
                    'crawl_date': crawl_date,
                    'path_file': path_json,
                    'category': category,
                    'article': articles

                }
                # print (result)
                # break
                self.a = self.a + 1
                with open(self.path+"/html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                    outfile.write(str(soup))
                with open(self.path+"/json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf_8_sig') as outfile:
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
