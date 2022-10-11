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
import os


class BjNews:

    def telegram_bot_sendtext(self, bot_message):
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
        Path(self.path + self.site_name + "/html/" + crawl_date + "/" + category + "/" + sub_category + "/").mkdir(
            parents=True, exist_ok=True)
        Path(self.path + self.site_name + "/json/" + crawl_date + "/" + category + "/" + sub_category + "/").mkdir(
            parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return crawl_date

    def get_browser(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")  # linux only
        chrome_options.add_argument("--headless")
        chrome_options.headless = True  # also works
        browser = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')

        browser.maximize_window()
        return browser

    def __init__(self):
        self.base_link = "https://www.sinarharian.com.my/"
        self.a = 0
        self.random_sleep = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.proxies = {'http': 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        # self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
        self.site_name = "sinarharian"

    def get_items(self):
        newpath = "/home/news/nst/json/20210317"
        for root, dir, files in os.walk(newpath):

            for file in files:
                # i=0
                print(file)
                root2 = root.replace("nst", "nst2")
                data21 = json.load(open(os.path.join(root, file), encoding='utf-8-sig'))
                location21 = data21['content'].split(": ")

                location = location21[0].strip()
                if "Ayisy Yusof" in location:
                    location=location.replace("Ayisy Yusof","")
                try:
                    content = location21[1].strip()
                except:
                    location = ""

                    content = location21[0].strip()

                if len(location) > 100:
                    location = ""
                    content = data21['content']
                result = {

                    "title": data21['title'],
                    "ndate": data21['ndate'],
                    "category": data21['category'],
                    "location": location,
                    "content": content,
                    "author": data21['author'],
                    "sitename": data21['sitename'],
                    "date_crawl": data21['date_crawl'],
                    "path_html": data21['path_html'],
                    "url": data21['url']

                }
                Path(root2).mkdir(parents=True, exist_ok=True)
                with open(root2 + "/" + file, 'w', encoding='utf8') as outfile:
                    json.dump(result, outfile, ensure_ascii=False)

        # print(result)

        # message = "Engine : Bj News  \n" + "Data : " + str(self.a)
        # self.telegram_bot_sendtext(str(message))


BjNews().get_items()

