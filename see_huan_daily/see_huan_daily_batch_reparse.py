import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import os
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
                response = requests.get(send_text)
                break
            except requests.exceptions.RequestException as e:
                print("gagal kirim telegram")
                continue

        return response.json()

    def create_folder(self, crawl_date, category):
        Path(self.path +"/batch2/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path +"/batch2/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "http://news.seehua.com/"
        self.website = "see_huan_daily"
        self.a = 0
        self.random_sleep = [1, 2, 3]
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
        self.path = "/news_cn/requests/news/"+ self.website

    def get_items(self):
        crawl_date = "20210302"
        for root, dir, files in os.walk(self.path + "/batch/html/" + crawl_date):
            for file in files:
                # i=0
                category = root
                category = category.split("/")
                category = category[8]

                self.create_folder(crawl_date, category)

                with open(os.path.join(root, file), encoding='utf_8_sig') as z:
                    name_file = file.replace(".html", "")
                    html = z.read()
                    try:
                        soup = BeautifulSoup(html, "html.parser")

                        title = soup.find("h1", class_="entry-title").get_text().replace("\n", "")
                        url = soup.find("meta", property="og:url")['content']

                        articles = soup.findAll("p")
                        article = ""
                        for article21 in articles:
                            article = article + article21.get_text().replace("\n", "")

                        ndate = soup.find("time", class_="entry-date updated td-module-date").attrs.get(
                            "datetime").split("T")
                        ndate = ndate[0].replace("-", "")


                        path_html = self.path + "/batch/html/" + crawl_date + "/" + category + "/" + name_file + ".html"

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

                        with open(self.path + "/batch2/json/" + crawl_date + "/" + category + "/" + name_file + ".json",
                                  'w', encoding='utf_8_sig') as outfile:
                            json.dump(result, outfile, ensure_ascii=False)
                        print("jumlah data: " + str(self.a))
                        print("category : " + category)
                    except:
                        continue



Kwong().get_items()