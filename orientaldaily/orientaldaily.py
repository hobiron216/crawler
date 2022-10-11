import hashlib
import time

import requests
from pathlib import Path

import re
import bs4
from datetime import  date
from requests.exceptions import Timeout
import random
import multiprocessing
import json
# import cloudscraper


class Sinchew:
    def telegram_bot_sendtext(self,bot_message):
        global response
        bot_token = '1381123927:AAEQ169ZfG5qQMvPaNaFyt8zBJzyeZ-feXc'
        bot_chatID = '1008898421'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        while True:
            try:
                response = requests.get(send_text,timeout=10)
                break
            except requests.exceptions.RequestException as e:
                print("gagal kirim telegram")
                continue

        return response.json()

    def create_folder(self,crawl_date,type):
        # Path("/home/shahid/Documents/requests/news/sinchew/html/"+ crawl_date+ "/world/").mkdir(parents=True, exist_ok=True)
        # Path("/home/shahid/Documents/requests/news/sinchew/json/" + crawl_date + "/world/").mkdir(parents=True, exist_ok=True)
        Path(self.path+"html/"+ crawl_date+ "/" + type + "/").mkdir(parents=True, exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + type + "/").mkdir(parents=True, exist_ok=True)
        # Path("/home/crawler/berita_cina/sinchew/except/"+ crawl_date).mkdir(parents=True, exist_ok=True)
        # "/dataph/requests/news/sinchew/html/" + crawl_date + "/world/" + href21 + ".html"

    def __init__(self):
        self.a = 0
        self.random_sleep= [1,2,3,4]
        # self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.proxies = {'http': 'http://pxuser:r@h@s!@2o2o@159.65.3.103:8252'}
        #self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        self.path="/news_cn/requests/news/orientaldaily/"
        self.link_fail=[]
        self.test=1
        self.list_link2 = []



    def get_items(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        categorys = ['advertorial','business', 'entertainment', 'international', 'local', 'nation', 'society']
        print ("====================================================" + crawl_date + "============================================================")
        for category in categorys :
            if category == 'advertorial':
                url = "https://www.orientaldaily.com.my/news/advertorial?page="
                self.get_html(category, url, crawl_date)
            elif category == 'business':
                url = "https://www.orientaldaily.com.my/news/business?page="
                self.get_html(category, url, crawl_date)
            elif category == 'entertainment':
                url = "https://www.orientaldaily.com.my/news/entertainment?page="
                self.get_html(category, url, crawl_date)
            elif category == 'international':
                url = "https://www.orientaldaily.com.my/news/international?page="
                self.get_html(category, url, crawl_date)
            elif category == 'local':
                url = "https://www.orientaldaily.com.my/news/local?page="
                self.get_html(category, url, crawl_date)
            elif category == 'nation':
                url = "https://www.orientaldaily.com.my/news/nation?page="
                self.get_html(category, url, crawl_date)
            elif category == 'society':
                url = "https://www.orientaldaily.com.my/news/society?page="
                self.get_html(category, url, crawl_date)




        message = "Engine : orientaldaily  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))

        # with open(self.path + "/cek_url.json", 'w', encoding='utf_8_sig') as outfile:
        #     json.dump(self.list_link2, outfile, ensure_ascii=False)
        # # print(len(self.link_fail))
        # # with open('/home/crawler/berita_cina/sinchew/except/'+ crawl_date+'/'+ 'except1.json', 'w') as outfile:
        # #     json.dump(self.link_fail, outfile)
        #
        # return type

    def get_html(self,category, url, crawl_date):
        self.create_folder(crawl_date, category)
        print(category)
        for page in range(1,16) : #1,6
            url21 = url + str(page)
            time.sleep(random.choice(self.random_sleep))
            user_agent = random.choice(self.user_agents)

            headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.9,id;q=0.8",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'upgrade-insecure-requests': "1",
            'user-agent': user_agent,
            'cookie': 'ncbi_sid=CE899787D9195471_2562SID; pmc.article.report=; _ga=GA1.2.1661002836.1569822027; entrezSort=pmc:; _gid=GA1.2.2059851631.1569998064; WebEnv=1zGUsr%40CE899787D9195471_2562SID; _gat_ncbiSg=1; _gat_dap=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAc+AzPgAwDsAIgJwAstAQtqQIynsccBsLlpRDLgDoAtnACsIADQgArgDsANgHsAhqnlQAHgBdMoAEyZwIgMbSQRY2DMXaxncvMzJWAPTIAzp9lRPbogNWciI3Cy5jaFNlCHQZIOM8fEoAQVoDKjpxMgM2Tk58Ay5SWnxxUQkLXOszDBtTDEcGj29ff0Dg0KqjLAB3fqF5UwAjZEHFEUHkRCEAc2UYKupjFiIuCJkiUmNyLnwLIhYVraPNnpByegOrLAAzVUVPKAP7LB0IXwP9rAPlrHJqGxAfsZLRtv9ASwWNRyHYbiBSEIikJTiArlgFCp1JpdHZXCBUeJ4atWBZxK8CdRJC4Ilhti5YXTwkd/iAAL5soA'
            }
            while True:
                try:
                    response = requests.get(url21,timeout=10,headers=headers, proxies=self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            title_link = []
            for index in soup.find_all('a', class_='link'):
                title = index.get('title')
                link = index.get('href')
                title_link.append(link)


            self.get_parser(category, title_link, crawl_date, page)



    def get_parser(self, category, title_link, crawl_date, page):
        for url in title_link:
            time.sleep(random.choice(self.random_sleep))
            user_agent = random.choice(self.user_agents)
            print("url : " + url)
            headers = {
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                'accept-encoding': "gzip, deflate",
                'accept-language': "en-US,en;q=0.9,id;q=0.8",
                'cache-control': "no-cache",
                'connection': "keep-alive",
                'upgrade-insecure-requests': "1",
                'user-agent': user_agent,
                'cookie': 'ncbi_sid=CE899787D9195471_2562SID; pmc.article.report=; _ga=GA1.2.1661002836.1569822027; entrezSort=pmc:; _gid=GA1.2.2059851631.1569998064; WebEnv=1zGUsr%40CE899787D9195471_2562SID; _gat_ncbiSg=1; _gat_dap=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAc+AzPgAwDsAIgJwAstAQtqQIynsccBsLlpRDLgDoAtnACsIADQgArgDsANgHsAhqnlQAHgBdMoAEyZwIgMbSQRY2DMXaxncvMzJWAPTIAzp9lRPbogNWciI3Cy5jaFNlCHQZIOM8fEoAQVoDKjpxMgM2Tk58Ay5SWnxxUQkLXOszDBtTDEcGj29ff0Dg0KqjLAB3fqF5UwAjZEHFEUHkRCEAc2UYKupjFiIuCJkiUmNyLnwLIhYVraPNnpByegOrLAAzVUVPKAP7LB0IXwP9rAPlrHJqGxAfsZLRtv9ASwWNRyHYbiBSEIikJTiArlgFCp1JpdHZXCBUeJ4atWBZxK8CdRJC4Ilhti5YXTwkd/iAAL5soA'
            }

            while True:
                try:
                    response_detail = requests.get(url, proxies=self.proxies, headers=headers)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue


            # ---------parsing url, title, date, article to json--------#
            sp_detail = bs4.BeautifulSoup(response_detail.content, "html.parser")
            detail_title = sp_detail.title.text
            # print(detail_title)
            detail_url = sp_detail.find("meta", property="og:url")['content']
            # print(detail_url)
            sub_date = detail_url.split('/')
            detail_date = sub_date[5] + '-' + sub_date[6] + '-' + sub_date[7]
            detail_id = sub_date[8]
            # print(detail_date)
            detail_article = sp_detail.select('.article.story>p')
            # 	print(detail_article)
            json_data = {'title': detail_title, 'url': detail_url, 'date': detail_date, 'article': detail_article}

            # print(str(json_data))

            self.a = self.a + 1

            href21 = hash(url)

            print("jumlah data : " + str(self.a))
            print("category : " + category)
            print("page :" + str(page))


            with open(self.path+"html/" + crawl_date + "/" + category + "/detail_" + str(href21) +'.html', 'w',encoding='utf_8_sig') as outfile:
                 outfile.write(str(response_detail.text))
            with open(self.path+"json/" + crawl_date + "/" + category + "/detail_" + str(href21) +'.json', 'w', encoding='utf_8_sig') as outfile:
                 outfile.write(str(json_data))




Sinchew().get_items()
#print(Sinchew().get_items())
