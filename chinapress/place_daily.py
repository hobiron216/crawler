import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
# import cloudscraper

import time
import random
import os
import codecs
class Chinapress:

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
        Path(self.path + "/" + category + "/" + sub_category).mkdir(parents=True,exist_ok=True)
        Path(self.path + "/" + category + "/" + sub_category).mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.chinapress.com.my/category/"
        self.website = "chinapress"
        self.a = 0
        self.random_sleep = [1, 2,3,4,5,6]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        # self.proxies2 = {'https': 'https://pxuser:r@h@s!@2o2o@159.65.3.103:8252',
        #                  'http': 'http://pxuser:r@h@s!@2o2o@159.65.3.103:8252'}
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
        self.path = "/news_cn/requests/news/chinapress/"
        # self.scraper = cloudscraper.create_scraper()
        self.today = date.today()

    def get_items(self):
        categorys = ['region']
        sub_categorys = ['kl', 'johor', 'northern', 'east_coast', 'negeri_sembilan', 'melaka', 'perak']

        for category in categorys:
            crawl_date = self.crawl_date()
            sub_category2=""
            if category=='region':
                for sub_category in sub_categorys:
                    if sub_category == "kl" :
                        # continue
                        url = "https://kl.chinapress.com.my/category/hot视频/page/"
                        self.get_url(url, category, crawl_date, sub_category, sub_category2)
                    elif sub_category == "johor" :
                        url = "https://johor.chinapress.com.my/category/johor人/page/"
                        self.get_url(url, category, crawl_date, sub_category, sub_category2)
                    elif sub_category == "northern" :
                        sub_categorys2 = ['penang_island', 'perai', 'jibo']
                        for sub_category2 in sub_categorys2:
                            if sub_category2 == 'penang_island':
                                url = "https://penang.chinapress.com.my/category/%e4%bb%8a%e6%97%a5%e5%8c%97%e9%a6%ac/%e6%a7%9f%e5%b2%9b/page/"
                                self.get_url(url, category, crawl_date, sub_category, sub_category2)
                            elif sub_category2 == 'perai':
                                url = "https://penang.chinapress.com.my/category/%e4%bb%8a%e6%97%a5%e5%8c%97%e9%a6%ac/%e5%a8%81%e7%9c%81/page/"
                                self.get_url(url, category, crawl_date, sub_category, sub_category2)
                            elif sub_category2 == 'jibo':
                                url = "https://penang.chinapress.com.my/category/%e4%bb%8a%e6%97%a5%e5%8c%97%e9%a6%ac/%e5%90%89%e7%8e%bb/page/"
                                self.get_url(url, category, crawl_date, sub_category, sub_category2)
                    elif sub_category == "east_coast" :
                        sub_categorys2 = ['pahang', 'kelantan', 'terengganu']
                        for sub_category2 in sub_categorys2:
                            if sub_category2 == 'pahang':
                                url = "https://eastcoast.chinapress.com.my/category/%e4%bb%8a%e6%97%a5%e4%b8%9c%e6%b5%b7%e5%b2%b8/%e5%bd%ad%e4%ba%a8/page/"
                                self.get_url(url, category, crawl_date, sub_category, sub_category2)
                            elif sub_category2 == 'kelantan':
                                url = "https://eastcoast.chinapress.com.my/category/%e4%bb%8a%e6%97%a5%e4%b8%9c%e6%b5%b7%e5%b2%b8/%e5%90%89%e5%85%b0%e4%b8%b9/page/"
                                self.get_url(url, category, crawl_date, sub_category, sub_category2)
                            elif sub_category2 == 'terengganu':
                                url = "https://eastcoast.chinapress.com.my/category/%e4%bb%8a%e6%97%a5%e4%b8%9c%e6%b5%b7%e5%b2%b8/%e7%99%bb%e5%98%89%e6%a5%bc/page/"
                                self.get_url(url, category, crawl_date, sub_category, sub_category2)

                    elif sub_category == "negeri_sembilan" :

                        sub_category2 = ""
                        url = "https://n9.chinapress.com.my/category/森州人/page/"
                        self.get_url(url, category, crawl_date, sub_category, sub_category2)
                    elif sub_category == "melaka" :
                        sub_category2 = ""
                        url = "https://mk.chinapress.com.my/category/melaka人/page/"
                        self.get_url(url, category, crawl_date, sub_category, sub_category2)
                    elif sub_category == "perak" :
                        sub_category2 = ""
                        url = "https://perak.chinapress.com.my/category/perak人/page/"
                        self.get_url(url, category, crawl_date, sub_category, sub_category2)
                    # elif sub_category == "china_news_hotline" :
                    #     url = self.base_link + "地方/中国报热线/page/"
                    #     self.get_url(url, category, crawl_date, sub_category, sub_category2)


        message = "Engine : placedaily \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))

        with open(self.path + "/json/cek_url_place.json", 'w', encoding='utf_8_sig') as outfile:
            json.dump(self.list_link2, outfile, ensure_ascii=False)

    def get_url (self, url, category, crawl_date, sub_category, sub_category2):
        # self.create_folder(crawl_date, category, sub_category)
        # page=0
        for page in range(1,21):#1,5052
            url21 = url + str(page)
            time.sleep(random.choice(self.random_sleep))
            user_agent = random.choice(self.user_agents)
            headers = {
                'authority': 'www.chinapress.com.my',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': '_ga=GA1.3.1562908727.1634786441; _gid=GA1.3.512005147.1634786441; __ssds=3; __ssuzjsr3=a9be0cd8e; __uzmaj3=1bd9dcf4-e783-45d5-b225-b559b1376e47; __uzmbj3=1634786444; _fbp=fb.2.1634786447713.741337500; aawp_id=9f87162603d8c305d0a73678aad06e36; iUUID=19a2cac94b1bb092d6d554a797f6f15d; innity.dmp.109.sess.id=221394904.109.1634786468306; innity.dmp.cks.innity=1; freq.5e661e8b47e7043d03000003=1; freq.5f462d2c47e7044a01000002=1; freq.616d4ff447e704bf15000006=1; innity.dmp.1.sess.id=221394904.1.1634786502784; innity.dmp.1.sess=2.1634786502784.1634786502784.1634786502855; dable_uid=37221179.1605116191217; __cf_bm=lFnC8Xzzh28oRTIynhE4YinaINFpSE9m1el5gt4kDGU-1634787401-0-AQ34GwQEeqh6VdksWAN5ZsxU0I2tWJH8HilpiMfLF3MRvul0GapCF6+x2PevzWZaNuL6q7WNYH7YBRD6Am3zMad7rpDewUD9V8/WXZH53GDTC/C4wXuD09gpNd8d9xgjbA==; innity.dmp.109.sess=32.1634786468306.1634787712444.1634787715918; __uzmcj3=3580810380683; __uzmdj3=1634787715; __gads=ID=56102bdfa915cbc1:T=1634786469:S=ALNI_MYI0PHpxa1QED0xPcLQfBeY0y9_6g; _gat_UA-64498512-1=1',
            }
            while True:
                try:
                    r = requests.get(url21, headers = headers, timeout = 5, proxies = self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            html=r.text


            soup=BeautifulSoup(html,'html.parser')
            divs=soup.find_all("div", class_='category_page_post clearfix')

            for div in divs:
                href = div.find("a").attrs.get('href')
                self.list_link.append(href)

            if not self.list_link:
                break
            self.parser(crawl_date, category, page, sub_category, sub_category2)
            self.list_link.clear()

    def parser(self, crawl_date, category, page,  sub_category, sub_category2):
        for url in self.list_link:
            try :
                time.sleep(random.choice(self.random_sleep))
                print("url : " + url)
                user_agent = random.choice(self.user_agents)
                headers = {
                    'authority': 'www.chinapress.com.my',
                    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'upgrade-insecure-requests': '1',
                    'user-agent': user_agent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                    'cookie': '_ga=GA1.3.1562908727.1634786441; _gid=GA1.3.512005147.1634786441; __ssds=3; __ssuzjsr3=a9be0cd8e; __uzmaj3=1bd9dcf4-e783-45d5-b225-b559b1376e47; __uzmbj3=1634786444; _fbp=fb.2.1634786447713.741337500; aawp_id=9f87162603d8c305d0a73678aad06e36; iUUID=19a2cac94b1bb092d6d554a797f6f15d; innity.dmp.109.sess.id=221394904.109.1634786468306; innity.dmp.cks.innity=1; freq.5e661e8b47e7043d03000003=1; freq.5f462d2c47e7044a01000002=1; freq.616d4ff447e704bf15000006=1; innity.dmp.1.sess.id=221394904.1.1634786502784; innity.dmp.1.sess=2.1634786502784.1634786502784.1634786502855; dable_uid=37221179.1605116191217; __cf_bm=lFnC8Xzzh28oRTIynhE4YinaINFpSE9m1el5gt4kDGU-1634787401-0-AQ34GwQEeqh6VdksWAN5ZsxU0I2tWJH8HilpiMfLF3MRvul0GapCF6+x2PevzWZaNuL6q7WNYH7YBRD6Am3zMad7rpDewUD9V8/WXZH53GDTC/C4wXuD09gpNd8d9xgjbA==; innity.dmp.109.sess=32.1634786468306.1634787712444.1634787715918; __uzmcj3=3580810380683; __uzmdj3=1634787715; __gads=ID=56102bdfa915cbc1:T=1634786469:S=ALNI_MYI0PHpxa1QED0xPcLQfBeY0y9_6g; _gat_UA-64498512-1=1',
                }
                while True:
                    try:
                        response_detail = requests.get(url, headers=headers, timeout=5, proxies = self.proxies)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue
                response_detail.encoding = 'utf-8'
                html = response_detail.text
                sp_detail = BeautifulSoup(html, "html.parser")

                detail_title = sp_detail.title.text
                detail_title = detail_title.split('|')[0]
                # print('Title : ' + detail_title)
                # detail_url = sp_detail.find("meta",  property="og:url")['content']
                # print('Url : ' + detail_url)
                sub_date = url.split('/')[-3]
                # print('Date : ' + sub_date)
                detail_article = sp_detail.select('.entry-content.clearfix>p')
                # print(str(detail_article))
                detail_id = sp_detail.find('div', id='post_id').text
                # print(detail_id)
                json_data = {'title': detail_title, 'url': url, 'date': sub_date, 'article': str(detail_article)}


                self.a = self.a + 1
                if not sub_category2:
                    filename_content = self.path + "/html/content/{}/{}-{}/detail_{}.html".format(self.today, category, sub_category, hash(url))
                    os.makedirs(os.path.dirname(filename_content), exist_ok=True)
                    with open(filename_content, 'w', encoding='utf_8_sig') as f:
                        f.write(str(response_detail.text))

                    filename_json = self.path + "/json/content/{}/{}-{}/detail_{}.json".format(self.today, category, sub_category, hash(url))
                    os.makedirs(os.path.dirname(filename_json), exist_ok=True)
                    with codecs.open(filename_json, 'w', encoding="utf_8_sig") as f:
                        f.write(str(json_data))
                else:
                    filename_content = self.path + "/html/content/{}/{}-{}-{}/detail_{}.html".format(self.today, category, sub_category, sub_category2, hash(url))
                    os.makedirs(os.path.dirname(filename_content), exist_ok=True)
                    with open(filename_content, 'w', encoding='utf_8_sig') as f:
                        f.write(str(response_detail.text))

                    filename_json = self.path + "/json/content/{}/{}-{}-{}/detail_{}.json".format(self.today, category, sub_category, sub_category2, hash(url))
                    os.makedirs(os.path.dirname(filename_json), exist_ok=True)
                    with codecs.open(filename_json, 'w', encoding="utf_8_sig") as f:
                        f.write(str(json_data))

                print("jumlah data: " + str(self.a))
                print("sub_category : " + sub_category)

                if sub_category2:
                    print("sub_category2 : " + sub_category2)
                print("page : " + str(page))
                self.list_link2.append(url)
                # break
            except Exception as e :
                print(e)
                continue


Chinapress().get_items()
