import hashlib
import json
import sys

import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
# import cloudscraper

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
        self.base_link = "https://www.newpages.com.my/v2/en/classified/0/classified.html"
        self.website = "newpages"
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
        # self.scraper = cloudscraper.create_scraper()

    def get_items(self):

        self.get_url(self.base_link)

    def get_url (self, url):

        user_agent = random.choice(self.user_agents)
        headers = {
            'authority': 'news.seehua.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cookie': '_ga=GA1.2.1626096402.1614575311; _pubcid=d923d344-351b-4bbd-88ac-8f37427c5927; _ss_pp_id=95f5312075774dd80751608237750435; __cfduid=d377d558eca47bac37c6c37741cd6d04e1618885457; cf_chl_prog=a10; cf_clearance=3210024770c3fbff44ef15410e681c69abe978b4-1618885484-0-250; __cf_bm=b9a93bb3855603e249b7bb0cc065bc7e57501e86-1618885488-1800-AQ6Wis70Iwqo7BgmF79uGrgkvov09S6BLBYXMZqogoIbVCchJKugksFgco+mbeowNDUGn4Jam7noKU3GXoNpjeEdGDRHFB4MzR8ypwrp9LE3NztJgxyA6MTjVWEbvrzL3A==; _gid=GA1.2.1356777591.1618885488; _pbjs_userid_consent_data=3524755945110770; cto_bidid=ELWihF8xS1paemNWY2dqeCUyRmVLaHRxRm1URjhYb2NTM2dDazhSJTJCWW5qV090YXBSSzJObFJFcnNEU3klMkZHYThJS2dVcEpqaXJWbUFBTmUlMkZVaERFVmJnQlBjdkt0R1IweExRZzAxM0xQNHJ3WlNVcUVzJTNE; cto_bundle=x2QZTV9tazg2M3BNYXU5VjJqZlJlayUyQmtJNmVpUHNXSGtwQkl2T0hBVXE5M1dKeWRMNDVHOGQxVFhwb0RiSVJ1SzYyUXRmc3RYZUJjM2p3QThTcW5yWmlEdiUyQnBDUXJ0ZHRRcmVxTVAwSHFlTUtnV1A3ZnNtRWxJRkFCTXRrZG9HeGxpakFvSHhjV0J1Q2dYNkZNRmVHOEswVzd3JTNEJTNE; _td=334bf114-dbd4-4607-9706-32a45b6d6b2a; __gads=ID=bc681a0b43e0fd7a:T=1618885516:S=ALNI_MZJEbQETFWfVqTfYqD6oPxvZgsI-A',
            'if-modified-since': 'Tue, 20 Apr 2021 01:30:58 GMT',
        }
        print("get url : " + url)

        while True:
            try:
                r =requests.get(url, timeout=10, headers=headers, proxies=self.proxies)
                break
            except requests.exceptions.RequestException as e:
                print("connetion timeout")
                continue


        html=r.text
        soup=BeautifulSoup(html,'html.parser')

        print("save html index")
        Path(self.path + "/").mkdir(parents=True, exist_ok=True)
        with open(self.path + "/" + "index.html", 'w', encoding='utf8') as outfile:
            outfile.write(str(soup))

        print("crawl index url")
        divs=soup.find_all("a")

        for div in divs:
            try :
                href = div.attrs.get('href')

                if ".." in href:
                    href = href.replace("..","")
                if "mailto:" in href:
                    continue
                if "jpg" in href or "png" in href:
                    continue
                if "JPG" in href or "PNG" in href:
                    continue
                if "www." in href:
                    continue
                if href == "#":
                    continue
                if "tel:" in href:
                    continue

                if "https:" in href or "http:" in href :
                    continue



                else:
                    if"#" in href:
                        href = "https://www.newpages.com.my/v2/en/classified/0/classified.html" + href
                    else:
                        href = "https://www.newpages.com.my" + href
                    if href not in self.list_link_check:

                        self.list_link.append(href)
                    else:
                        continue
            except:
                continue

        self.url_detail()

    def url_detail(self):

        for url in self.list_link:
            if url =="https://www.newpages.com.my/":
                continue

            if url in self.list_link_check:
                continue

            self.list_link_check.append(url)
            print("move to url : " + url)
            last_string_url = url[-1]
            url_split = url.split("/")

            if last_string_url == "/" :
                nama_file = url_split[-2].strip()
            else:
                nama_file = url_split[-1].strip()

            category = url.replace("https://www.newpages.com.my/", "").replace(nama_file, "")

            self.create_folder(category)

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
            b = 0
            while True:
                b = b + 1
                if b > 5:
                    break
                try:
                    r =requests.get(url, timeout=10, headers=headers, proxies=self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            if b > 5:
                continue
            r.encoding = 'utf-8'
            html = r.text
            soup = BeautifulSoup(html, "html.parser")

            print("save html")
            with open(self.path + "/" + category + "/" + nama_file + ".html", 'w', encoding='utf8') as outfile:
                outfile.write(str(soup))

            print("crawl url")

            divs = soup.find_all("a")
            list_url=[]
            for div in divs:
                try:
                    href = div.attrs.get('href')

                    if ".." in href:
                        href = href.replace("..", "")
                    if "mailto:" in href:
                        continue
                    if "jpg" in href or "png" in href:
                        continue
                    if "JPG" in href or "PNG" in href:
                        continue
                    if "www." in href:
                        continue
                    if href == "#":
                        continue
                    if "tel:" in href:
                        continue
                    if "https:" in href or "http:" in href:
                        continue

                    else:
                        if "#" in href:
                            href = "https://www.newpages.com.my/v2/en/classified/0/classified.html" + href
                        else:
                            href = "https://www.newpages.com.my" + href

                        if href not in self.list_link_check:
                            list_url.append(href)
                        else:
                            continue
                except:
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
                try:
                    if url == "https://www.newpages.com.my/":
                        continue
                    if url in self.list_link_check:
                        continue

                    self.list_link_check.append(url)
                    # print("detail_category : " + nama_file21)
                    print("move to url loop : " + url)
                    # self.list_link_check.append(url)
                    last_string_url = url[-1]
                    url_split = url.split("/")

                    if last_string_url == "/":
                        nama_file = url_split[-2].strip()
                    else:
                        nama_file = url_split[-1].strip()


                    category = url.replace("https://www.newpages.com.my/", "").replace(nama_file, "")

                    self.create_folder(category)

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

                    b = 0
                    while True:
                        b = b + 1
                        if b > 5:
                            break
                        try:
                            r = requests.get(url, timeout=10, headers=headers, proxies=self.proxies)
                            break
                        except requests.exceptions.RequestException as e:
                            print(url)
                            continue
                    if b > 5 :
                        continue
                    r.encoding = 'utf-8'
                    html = r.text
                    soup = BeautifulSoup(html, "html.parser")

                    print("save html")
                    with open(self.path + "/" + category + "/" + nama_file + ".html", 'w', encoding='utf8') as outfile:
                        outfile.write(str(soup))

                    print("crawl url")

                    divs = soup.find_all("a")

                    for div in divs:
                        try:
                            href = div.attrs.get('href')

                            if ".." in href:
                                href = href.replace("..", "")
                            if "mailto:" in href:
                                continue
                            if "jpg" in href or "png" in href:
                                continue
                            if "JPG" in href or "PNG" in href:
                                continue
                            if "www." in href:
                                continue
                            if href == "#":
                                continue
                            if "tel:" in href:
                                continue
                            if "https:" in href or "http:" in href:
                                continue

                            else:

                                if "#" in href:
                                    href = "https://www.newpages.com.my/v2/en/classified/0/classified.html" + href
                                else:
                                    href = "https://www.newpages.com.my" + href

                                if href not in self.list_link_check:
                                    list_url.append(href)
                                else:
                                    continue


                        except:
                            continue
                except:
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
