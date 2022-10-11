import hashlib
import json
import sys

import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import cloudscraper

import time
import random


class Spider:
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

    def create_folder(self, category):
        Path(self.path +"/" + category + "/").mkdir(parents=True,exist_ok=True)


    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.yellowpages.my/"
        self.website = "yellowpages"
        self.a = 0
        self.random_sleep = [0.5, 1.4, 2.1]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.proxies2 = {'https': 'https://pxuser:r@h@s!@2o2o@159.65.3.103:8252',
                         'http': 'http://pxuser:r@h@s!@2o2o@159.65.3.103:8252'}
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
        self.list_link_check = []
        self.list_category = []
        self.path = "/dataph/one_time_crawling/home/"+ self.website
        self.scraper = cloudscraper.create_scraper(delay=5)

    def get_items(self):
        # r = self.scraper.get("https://yellowpages.my/national-cancer-society-of-malaysia")
        # html = r.text
        # print(html)
        # soup = BeautifulSoup(html, 'html.parser')
        # #
        # # divs = soup.find("div", class_="hover-menu").find_all("a")
        # #
        # # print(divs)
        # # for div in divs:
        # #     try:
        # #         print(div.attrs.get("href"))
        # #     except:
        # #         continue
        # with open("tes.html", 'w', encoding='utf8') as outfile:
        #     outfile.write(str(soup))
        # sys.exit()


        # all_category = ["https://yellowpages.my/services/l", "https://yellowpages.my/buysell/l", "https://yellowpages.my/jobs/l", "https://yellowpages.my/hireme/l", "https://yellowpages.my/education"]
        # for category21 in all_category:
        #     self.list_link_check.append(category21)

        while True:
            try:
                r = self.scraper.get(self.base_link)
                break
            except requests.exceptions.RequestException as e:
                print("connetion timeout")
                continue
        html = r.text
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')


        print("crawl general data")
        divs = soup.find("div", class_="content").find_all("a")
        for div in divs:
            href = div.attrs.get('href')
            if href == "/" or href == "/l":
                continue
            # print(href)
            if "www." in href:
                continue
            if "tel:+" in href:
                continue
            if "https:" in href or "http:" in href:
                continue

            else:
                href = "https://yellowpages.my" + href
                if href not in self.list_link_check:

                    self.list_link.append(href)

        for url in self.list_link:
            time.sleep(random.choice(self.random_sleep))
            self.list_link_check.append(url)
            while True:
                try:
                    r = self.scraper.get(url)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')

            last_string_url = url[-1]
            url_split = url.split("/")

            if last_string_url == "/":
                nama_file = url_split[-2].strip()
            else:
                nama_file = url_split[-1].strip()

            category = url.replace(nama_file, "").replace("https://yellowpages.my/", "")

            self.create_folder(category)
            with open(self.path + "/" + category + "/" +  nama_file + ".html", 'w', encoding='utf8') as outfile:
                outfile.write(str(soup))

        self.list_link.clear()
        self.get_url(self.base_link)

    def get_url (self, url):

        time.sleep(random.choice(self.random_sleep))
        print("get url : " + url)
        while True:
            try:
                r =self.scraper.get(url)
                break
            except requests.exceptions.RequestException as e:
                print("connetion timeout")
                continue
        html=r.text
        # print(html)
        soup=BeautifulSoup(html,'html.parser')

        print("save html index")
        Path(self.path + "/").mkdir(parents=True, exist_ok=True)
        with open(self.path + "/" + "index.html", 'w', encoding='utf8') as outfile:
            outfile.write(str(soup))

        print("crawl index url")
        divs=soup.find("div", class_="hover-menu").find_all("a")
        for div in divs:
            href = div.attrs.get('href')
            if "jpg" in href or "png" in href:
                continue
            if "JPG" in href or "PNG" in href:
                continue
            if href =="/" or href=="/l":
                continue
            if "www." in href:
                continue
            if "tel:+" in href:
                continue
            if "https:" in href or "http:" in href:
                continue

            else:
                href = "https://yellowpages.my" + href
                if href not in self.list_link_check:

                    self.list_link_check.append(href)
                    self.list_link.append(href)
                else:
                    continue

        # print(self.list_link)
        self.url_detail()

    def url_detail(self):

        for url in self.list_link:
            if url =="https://yellowpages.my/":
                continue
            if url == "https://yellowpages.my":
                continue
            if url == "https://yellowpages.my/l/":
                continue
            print("move to url : " + url)

            if url == "https://yellowpages.mytel:":
                continue

            if url == "https://yellowpages.mymailto:audit@smc76.com":
                continue
            if "@" in url:
                continue
            if "mytel" in url:
                continue

            if "/l/" in url:
                continue

            time.sleep(random.choice(self.random_sleep))
            b = 0
            while True:
                try:
                    b=b+1
                    if b>5:
                        break
                    r = self.scraper.get(url)
                    r.encoding = 'utf-8'
                    html = r.text
                    if "Error 502" in html:
                        continue
                    if "Bad gateway" in html:
                        continue
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            if b>5:
                continue
            soup = BeautifulSoup(html, "html.parser")

            print("save html")

            last_string_url = url[-1]
            url_split = url.split("/")

            if last_string_url == "/":
                nama_file = url_split[-3].strip()
            else:
                nama_file = url_split[-2].strip()

            category = url.replace("https://yellowpages.my/", "").replace("/l", "")
            # print(category)
            self.create_folder(category)
            with open(self.path + "/" + category + "/" +  nama_file + ".html", 'w', encoding='utf8') as outfile:
                outfile.write(str(soup))

            print("crawl url")

            divs = soup.find_all("div", class_="left-cont")
            list_url=[]
            for div in divs:
                href = div.find("a").attrs.get('href')
                if "jpg" in href or "png" in href:
                    continue
                if "JPG" in href or "PNG" in href:
                    continue
                if "www." in href:
                    continue
                if "tel:+" in href:
                    continue
                if "https:" in href or "http:" in href:
                    continue


                else:
                    href = "https://yellowpages.my" + href
                    if href not in self.list_link_check:

                        list_url.append(href)
                    else:
                        continue

            # print(list_url)
            if list_url:
                self.get_url_loop(list_url,nama_file)
            else:
                continue
    def get_url_loop(self, list_url, nama_file21):
        a=0
        list_url2=[]
        while True:
            for url in list_url:
                if url == "https://yellowpages.my/":
                    continue
                if url == "https://yellowpages.my":
                    continue
                if url == "https://yellowpages.my/l/":
                    continue

                if url =="https://yellowpages.mytel:":
                    continue
                if url =="https://yellowpages.mymailto:audit@smc76.com":
                    continue
                if "@" in url:
                    continue
                if "mytel" in url:
                    continue
                if "/l/" in url:
                    continue

                if url in self.list_link_check:
                    continue

                self.list_link_check.append(url)
                # print("detail_category : " + nama_file21)
                print("move to url loop : " + url)

                time.sleep(random.choice(self.random_sleep))
                b = 0
                while True:

                    try:
                        b=b+1
                        if b>5:
                            break
                        r = self.scraper.get(url)
                        r.encoding = 'utf-8'
                        html = r.text
                        if "Error 502" in html:
                            continue
                        if "Bad gateway" in html:
                            continue
                        break
                    except requests.exceptions.RequestException as e:
                        print(url)
                        continue
                if b>5:
                    continue
                r.encoding = 'utf-8'
                html = r.text
                soup = BeautifulSoup(html, "html.parser")

                print("save html")
                last_string_url = url[-1]
                url_split = url.split("/")

                if last_string_url == "/":
                    nama_file = url_split[-2].strip()
                else:
                    nama_file = url_split[-1].strip()

                category = url.replace("https://yellowpages.my/", "").replace(nama_file, "")

                self.create_folder(category)
                with open(self.path + "/" + category + "/" + nama_file + ".html", 'w', encoding='utf8') as outfile:
                    outfile.write(str(soup))


                print("crawl url")

                divs = soup.find_all("a")
                # print(html)

                for div in divs:
                    href = div.attrs.get('href')
                    if href:
                        if "jpg" in href or "png" in href:
                            continue
                        if "JPG" in href or "PNG" in href:
                            continue
                        if "www." in href:
                            continue
                        if "tel:+" in href:
                            continue
                        if "https:" in href or "http:" in href:
                            continue

                        else:
                            href = "https://yellowpages.my" + href
                            if href not in self.list_link_check:

                                list_url2.append(href)
                            else:
                                continue
                    else:
                        continue
            a=a+1
            print(a)
            if list_url2:
                # print(list_url2)
                list_url.clear()
                for data in list_url2:
                    list_url.append(data)
                list_url2.clear()
                continue
            else:
                break



Spider().get_items()
