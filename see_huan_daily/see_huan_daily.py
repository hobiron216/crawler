import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import cloudscraper

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
        return  crawl_date

    def __init__(self):
        self.base_link = "http://news.seehua.com/"
        self.website = "see_huan_daily"
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
        self.path = "/news_cn/requests/news/"+ self.website
        self.scraper = cloudscraper.create_scraper()

    def get_items(self):
        categorys = ['Sarawak', 'Sabah', 'Peninsular Malaysia', 'International', 'Sport', 'Entertainment', 'Technology', 'Finance','Opinion' ]

        for category in categorys:
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)
            if category=='Sarawak':
                url = "http://news.seehua.com/?cat=3"
                self.get_url(url, category, crawl_date)

            elif category=='Sabah' :
                url = "http://news.seehua.com/?cat=8"
                self.get_url(url, category, crawl_date)

            elif category=='Peninsular Malaysia' :
                url = "http://news.seehua.com/?cat=11"
                self.get_url(url, category, crawl_date)

            elif category=='International' :
                url = "http://news.seehua.com/?cat=12"
                self.get_url(url, category, crawl_date)

            elif category=='Sport' :
                url = "http://news.seehua.com/?cat=13"
                self.get_url(url, category, crawl_date)

            elif category == 'Entertainment':
                url = "http://news.seehua.com/?cat=15"
                self.get_url(url, category, crawl_date)

            elif category == 'Technology':
                url = "http://news.seehua.com/?cat=14"
                self.get_url(url, category, crawl_date)

            elif category == 'Finance':
                url = "http://news.seehua.com/?cat=18"
                self.get_url(url, category, crawl_date)

            elif category=='Opinion' :
                url = "http://news.seehua.com/?cat=28"
                self.get_url(url, category, crawl_date)



        message = "Engine : " + self.website + "\n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))



    def get_url (self, url, category, crawl_date):
        for page in range(1,4):
            a=True
            while a:
                url21 = url + "&paged=" + str(page)
                time.sleep(random.choice(self.random_sleep))
                user_agent = random.choice(self.user_agents)
                headers = {
                    'authority': 'news.seehua.com',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                    'cookie': '_ga=GA1.2.1626096402.1614575311; _pubcid=d923d344-351b-4bbd-88ac-8f37427c5927; _ss_pp_id=95f5312075774dd80751608237750435; __cfduid=d377d558eca47bac37c6c37741cd6d04e1618885457; cf_chl_prog=a10; cf_clearance=3210024770c3fbff44ef15410e681c69abe978b4-1618885484-0-250; __cf_bm=b9a93bb3855603e249b7bb0cc065bc7e57501e86-1618885488-1800-AQ6Wis70Iwqo7BgmF79uGrgkvov09S6BLBYXMZqogoIbVCchJKugksFgco+mbeowNDUGn4Jam7noKU3GXoNpjeEdGDRHFB4MzR8ypwrp9LE3NztJgxyA6MTjVWEbvrzL3A==; _gid=GA1.2.1356777591.1618885488; _pbjs_userid_consent_data=3524755945110770; cto_bidid=ELWihF8xS1paemNWY2dqeCUyRmVLaHRxRm1URjhYb2NTM2dDazhSJTJCWW5qV090YXBSSzJObFJFcnNEU3klMkZHYThJS2dVcEpqaXJWbUFBTmUlMkZVaERFVmJnQlBjdkt0R1IweExRZzAxM0xQNHJ3WlNVcUVzJTNE; cto_bundle=x2QZTV9tazg2M3BNYXU5VjJqZlJlayUyQmtJNmVpUHNXSGtwQkl2T0hBVXE5M1dKeWRMNDVHOGQxVFhwb0RiSVJ1SzYyUXRmc3RYZUJjM2p3QThTcW5yWmlEdiUyQnBDUXJ0ZHRRcmVxTVAwSHFlTUtnV1A3ZnNtRWxJRkFCTXRrZG9HeGxpakFvSHhjV0J1Q2dYNkZNRmVHOEswVzd3JTNEJTNE; _td=334bf114-dbd4-4607-9706-32a45b6d6b2a; __gads=ID=bc681a0b43e0fd7a:T=1618885516:S=ALNI_MZJEbQETFWfVqTfYqD6oPxvZgsI-A',
                    'if-modified-since': 'Tue, 20 Apr 2021 01:30:58 GMT',
                }
                while True:
                    try:
                        r = self.scraper.get(url21)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                html=r.text
                print(html)

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
                        r = self.scraper.get(url, timeout=50, proxies=self.proxies, headers=headers)
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

                ndate = soup.find("time", class_="entry-date updated td-module-date").attrs.get("datetime").split("T")
                ndate = ndate[0].replace("-","")



                href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                path_html = self.path+"/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

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
                with open(self.path+"/html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                    outfile.write(str(soup))
                with open(self.path+"/json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf_8_sig') as outfile:
                    json.dump(result, outfile, ensure_ascii=False)
                print("jumlah data: " + str(self.a))
                print("category : " + category)
                print("page : " + str(page))
                # break
            except Exception as e :
                print(e)
                continue


Kwong().get_items()
