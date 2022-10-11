import hashlib
import time

import requests
from pathlib import Path


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

        self.base_link = "https://www.chinapress.com.my/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5,6]
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
        self.path="/news_cn/requests/news/chinapress/"
        self.link_fail=[]
        self.test=1
        self.list_link2 = []



    def get_items(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        types = ['auditorium','domestic', 'entertainment', 'finance', 'latest_news', 'sport', 'supplement']
        print ("====================================================" + crawl_date + "============================================================")
        for type in types :
            # print(type)
            category=""
            url = ""


            if type=='auditorium':
                # continue
                sub_types = ['finance', 'full-of-air',  'local-column', 'photos',  'pieces']
                for sub_type in sub_types:
                    category = type + "-" + sub_type
                    if sub_type=="finance":
                        url = "https://www.chinapress.com.my/category/%e8%af%84%e8%ae%ba/page/qwerty?gpid=540877"
                    elif sub_type =="full-of-air":
                        url = "https://www.chinapress.com.my/category/%e8%af%84%e8%ae%ba/page/qwerty?gpid=540877"
                    elif sub_type == "local-column" :
                        url = "https://www.chinapress.com.my/category/%e8%af%84%e8%ae%ba/page/qwerty?gpid=537721"
                    elif sub_type == "photos" :
                        url = "https://www.chinapress.com.my/category/%e5%9b%be%e8%be%91/page/"
                    elif sub_type == "pieces":
                        url = "https://www.chinapress.com.my/category/%e5%b0%8f%e5%93%81/page/"
                    self.get_html(category, url, crawl_date)

            elif type == 'domestic':
                sub_types = ['court', 'current-events', 'dedication', 'political']
                for sub_type in sub_types:
                    # print(sub_type)
                    category = type + "-" + sub_type
                    if sub_type == "court":
                        url = "https://www.chinapress.com.my/category/%e6%b3%95%e5%ba%ad/page/"
                    elif sub_type == "current-events":
                        url = "https://www.chinapress.com.my/category/%e6%97%b6%e4%ba%8b/page/"
                    elif sub_type == "dedication":
                        url = "https://www.chinapress.com.my/category/%e7%8c%ae%e8%af%8d/page/"
                    elif sub_type == "political":
                        url = "https://www.chinapress.com.my/category/%e6%94%bf%e6%b2%bb/page/"
                    self.get_html(category, url, crawl_date)

            elif type == 'entertainment':
                sub_types = ['china-hongkong-taiwan', 'dare-to-speak', 'entertainment-palette', 'european-american', 'japanese-korean', 'ma-xin']
                for sub_type in sub_types:
                    category = type + "-" + sub_type
                    if sub_type == "china-hongkong-taiwan":
                        url = "https://www.chinapress.com.my/category/%e4%b8%ad%e6%b8%af%e5%8f%b0%e5%a8%b1%e4%b9%90/page/"
                    elif sub_type == "dare-to-speak":
                        url = "https://www.chinapress.com.my/category/%e5%a8%b1%e4%b9%90/%e7%a5%af%e8%af%9d%e6%95%a2%e6%95%a2%e8%ae%b2/"
                    elif sub_type == "entertainment-palette":
                        url = "https://www.chinapress.com.my/category/%e5%a8%b1%e4%b9%90%e8%b0%83%e8%89%b2%e7%9b%98/page/"
                    elif sub_type == "european-american":
                        url = "https://www.chinapress.com.my/category/%e6%ac%a7%e7%be%8e%e5%a8%b1%e4%b9%90/page/"
                    elif sub_type == "japanese-korean":
                        url = "https://www.chinapress.com.my/category/%e6%97%a5%e9%9f%a9%e5%a8%b1%e4%b9%90/page/"
                    elif sub_type == "ma-xin":
                        url = "https://www.chinapress.com.my/category/%e9%a9%ac%e6%96%b0%e5%a8%b1%e4%b9%90/page/"
                    self.get_html(category, url, crawl_date)

            elif type == 'finance':
                sub_types = ['budget', 'corperate-seminar', 'domestic-finance', 'enterprise', 'excellent-elite',
                             'financial-winner', 'global', 'news', 'pink-club', 'stock-market', 'turn-around']
                for sub_type in sub_types:
                    category = type + "-" + sub_type
                    if sub_type == "budget":
                        url = "https://www.chinapress.com.my/category/%e8%b2%a1%e6%94%bf%e9%a0%90%e7%ae%97%e6%a1%88/page/"
                    elif sub_type == "corperate-seminar":
                        url = "https://www.chinapress.com.my/category/%e4%bc%81%e6%a5%ad%e7%a0%94%e8%a8%8e%e6%9c%83/page/"
                    elif sub_type == "domestic-finance":
                        url = "https://www.chinapress.com.my/category/%e8%b4%a2%e7%bb%8f%e6%96%b0%e9%97%bb/page/"
                    elif sub_type == "enterprise":
                        url = "https://www.chinapress.com.my/category/%e4%bc%81%e4%b8%9a/page/"
                    elif sub_type == "excellent-elite":
                        url = "https://www.chinapress.com.my/category/%e8%b4%a2%e7%bb%8f/%e5%8d%93%e8%b6%8a%e7%b2%be%e8%8b%b1%e5%bd%95/"
                    elif sub_type == "financial-winner":
                        url = "https://www.chinapress.com.my/category/%e7%90%86%e8%b4%a2%e8%b5%a2%e5%ae%b6/page/"
                    elif sub_type == "global":
                        url = "https://www.chinapress.com.my/category/%e7%8e%af%e7%90%83/page/"
                    elif sub_type == "news":
                        url = "https://www.chinapress.com.my/category/%e5%95%86%e6%a5%ad%e8%b3%87%e8%a8%8a/page/"
                    elif sub_type == "pink-club":
                        url = "https://www.chinapress.com.my/category/%e7%b2%89%e7%ba%a2%e7%a4%be/page/"
                    elif sub_type == "stock-market":
                        url = "https://www.chinapress.com.my/category/%e8%82%a1%e5%b8%82/page/"
                    elif sub_type == "turn-around":
                        url = "https://www.chinapress.com.my/category/%e6%a5%bc%e8%bd%ac%e4%b9%be%e5%9d%a4/page/"
                    self.get_html(category, url, crawl_date)
                break
            elif type == 'latest_news':
                url = "https://www.chinapress.com.my/category/%E4%BB%8A%E6%97%A5%E6%8A%A2%E9%B2%9C%E7%9C%8B/page/"
                category = type
                self.get_html(category, url, crawl_date)

            elif type == 'sport':
                sub_types = ['athletics', 'badminton', 'basketball', 'bowling', 'comprehensive-games', 'football', 'other',
                             'ping-pong', 'racing-car', 'squash', 'swim', 'tennis']
                for sub_type in sub_types:
                    category = type + "-" + sub_type
                    if sub_type == "athletics":
                        url = "https://www.chinapress.com.my/category/%e7%94%b0%e5%be%84/page/"
                    elif sub_type == "badminton":
                        url = "https://www.chinapress.com.my/category/%e7%be%bd%e7%90%83/page/"
                    elif sub_type == "basketball":
                        url = "https://www.chinapress.com.my/category/%e7%af%ae%e7%90%83/page/"
                    elif sub_type == "bowling":
                        url = "https://www.chinapress.com.my/category/%e4%bf%9d%e9%be%84%e7%90%83/page/"
                    elif sub_type == "comprehensive-games":
                        url = "https://www.chinapress.com.my/category/%e7%bb%bc%e5%90%88%e5%9e%8b%e8%bf%90%e5%8a%a8%e4%bc%9a/page/"
                    elif sub_type == "football":
                        url = "https://www.chinapress.com.my/category/%e8%b6%b3%e7%90%83/page/"
                    elif sub_type == "other":
                        url = "https://www.chinapress.com.my/category/%e5%85%b6%e4%bb%96/page/"
                    elif sub_type == "ping-pong":
                        url = "https://www.chinapress.com.my/category/%e4%b9%92%e4%b9%93/page/"
                    elif sub_type == "racing-car":
                        url = "https://www.chinapress.com.my/category/%e8%b5%9b%e8%bd%a6/page/"
                    elif sub_type == "squash":
                        url = "https://www.chinapress.com.my/category/%e5%a3%81%e7%90%83/page/"
                    elif sub_type == "swim":
                        url = "https://www.chinapress.com.my/category/%e6%b8%b8%e6%b3%b3/page/"
                    elif sub_type == "tennis":
                        url = "https://www.chinapress.com.my/category/%e7%bd%91%e7%90%83/page/"
                    self.get_html(category, url, crawl_date)

            elif type == 'supplement':
                sub_types = ['car-power', 'family-fun', 'fashion', 'freely', 'health', 'learn',
                             'like-weekly', 'smart', 'taste', 'tourism']
                for sub_type in sub_types:
                    category = type + "-" + sub_type
                    if sub_type == "car-power":
                        url = "https://www.chinapress.com.my/category/%e8%bd%a6%e5%8a%a8%e5%8a%9b/page/"
                    elif sub_type == "family-fun":
                        url = "https://www.chinapress.com.my/category/%e5%b1%85%e5%ae%b6%e4%b9%90/page/"
                    elif sub_type == "fashion":
                        url = "https://www.chinapress.com.my/category/%e6%bd%ae%e9%85%b7/page/"
                    elif sub_type == "freely":
                        url = "https://www.chinapress.com.my/category/%e6%9e%b6%e5%8a%bf%e5%a0%82/page/"
                    elif sub_type == "health":
                        url = "https://www.chinapress.com.my/category/%e5%81%a5%e5%ba%b7%e7%82%b9/page/"
                    elif sub_type == "learn":
                        url = "https://www.chinapress.com.my/category/%e5%ad%a6%e4%b9%a0%e5%8a%9b/page/"
                    elif sub_type == "like-weekly":
                        url = "https://www.chinapress.com.my/category/like%e5%91%a8%e5%88%8a/page/"
                    elif sub_type == "smart":
                        url = "https://www.chinapress.com.my/category/%e6%b5%81%e5%8a%a8%e5%a4%af/page/"
                    elif sub_type == "taste":
                        url = "https://www.chinapress.com.my/category/%e5%a4%a7%e9%a3%9f%e5%a0%82/page/"
                    elif sub_type == "tourism":
                        url = "https://www.chinapress.com.my/category/%e5%a4%a7%e7%8e%a9%e5%ae%b6/page/"

                    self.get_html(category, url, crawl_date)
            sub_types.clear()

        message = "Engine : Chinapress  \n" + "Data : " + str(self.a)
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
        for page in range(1,6) : #1,6
            # break
            if "qwerty" in url:
                url21 = url.replace("qwerty", str(page))
            else:
                url21 = url + str(page)
            print(url21)
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
                    response = requests.get(url21,timeout=10)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue
            print(response.text)
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

            title_link = []
            for a in soup.select('.title a'):
                    link_detail = a['href']
                    title_link.append(link_detail)
            if not title_link:
                for a in soup.select('.category_page_post_content a'):
                    link_detail = a['href']
                    title_link.append(link_detail)


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
            detail_title = detail_title.split('|')[0]
            # print('Title : ' + detail_title)
            try :
                detail_url = sp_detail.find("meta", property="og:url")['content']
                # print('Url : ' + detail_url)
                sub_date = detail_url.split('/')[-3]
                # print('Date : ' + sub_date)
                detail_article = sp_detail.select('.entry-content.clearfix>p')
                # print(str(detail_article))
                detail_id = sp_detail.find('div', id='post_id').text
                # print(detail_id)
                json_data = {'title': detail_title, 'url': detail_url, 'date': sub_date, 'article': str(detail_article)}
            except:
                # detail_url = sp_detail.find("meta", property="og:url")['content']
                # print('Url : ' + detail_url)
                sub_date = url.split('/')[-3]
                # print('Date : ' + sub_date)
                detail_article = sp_detail.select('.entry-content.clearfix>p')
                # print(str(detail_article))
                detail_id = sp_detail.find('div', id='post_id').text
                # print(detail_id)
                json_data = {'title': detail_title, 'url': url, 'date': sub_date, 'article': str(detail_article)}

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
