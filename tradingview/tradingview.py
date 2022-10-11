import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import random
import time

class Merits:
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

    def create_folder(self, crawl_date, main_category, category):
        Path("/home/" + self.website + "/" + crawl_date + "/" + main_category + "/" + category).mkdir(parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.tradingview.com"
        self.website = "tradingview"
        self.a = 0
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        self.random_sleep = [1, 2, 3, 4, 5]
        self.result=[]

    def get_items(self):
        main_categorys = ['sector', 'industry']

        crawl_date = self.crawl_date()

        for main_category in main_categorys:
            if main_category == "sector":
                url = self.base_link + "/markets/stocks-indonesia/sectorandindustry-sector/"
                self.get_category(url)
                self.parser(self.list_link, crawl_date,main_category)
                self.list_link.clear()
                del self.list_link[:]


            else :
                url = self.base_link + "/markets/stocks-indonesia/sectorandindustry-industry/"
                self.get_category(url)
                self.parser(self.list_link, crawl_date, main_category)
                self.list_link.clear()
                del self.list_link[:]


            # print(self.list_link)

            # self.parser(self.list_link, crawl_date,main_category)
        # break

    def get_category(self, url):
        time.sleep(random.choice(self.random_sleep))
        user_agent = random.shuffle(self.user_agents)
        headers = {
            'authority': 'www.tradingview.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cookie': '_sp_ses.cf1a=*; _ga=GA1.2.311143034.1614222404; _gid=GA1.2.1624216106.1614222404; g_state={"i_p":1614229616015,"i_l":1}; _sp_id.cf1a=f7d6365e-ef11-4b0d-b0c9-c0e0a24f05eb.1614222403.1.1614223663.1614222403.86c8db40-1ed8-4365-bfbb-31bb870ce8b2; _gat_gtag_UA_24278967_1=1',
        }

        r = requests.get(url, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.findAll("tr", class_="tv-data-table__row tv-data-table__stroke tv-screener-table__result-row")
        for div in divs:
            href = div.find("a").attrs.get("href")
            category = div.find("a").get_text()
            link = self.base_link + href
            result = {
                "link": link,
                "category": category
            }
            self.list_link.append(result)

    def parser(self, list_link, crawl_date, main_category):

        for data in list_link:
            url = data['link']
            category = data['category']
            time.sleep(random.choice(self.random_sleep))
            user_agent = random.shuffle(self.user_agents)
            headers = {
                'authority': 'www.tradingview.com',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': '_sp_ses.cf1a=*; _ga=GA1.2.311143034.1614222404; _gid=GA1.2.1624216106.1614222404; g_state={"i_p":1614229616015,"i_l":1}; _sp_id.cf1a=f7d6365e-ef11-4b0d-b0c9-c0e0a24f05eb.1614222403.1.1614223663.1614222403.86c8db40-1ed8-4365-bfbb-31bb870ce8b2; _gat_gtag_UA_24278967_1=1',
            }

            r= requests.get(url, headers=headers)
            html = r.text
            soup21= BeautifulSoup(html, "html.parser")
            # if main_category != "sector":
            #     print(soup)
            soup21 = soup21.findAll("tr", class_="tv-data-table__row tv-data-table__stroke tv-screener-table__result-row")
            for soup in soup21:
                company = soup.find("a", class_="tv-screener__symbol").get_text()
                if main_category == "sector":
                    keterangan = soup.find("span", class_="tv-screener__symbol--secondary").get_text().replace("/n","").replace("/t","").replace("\n","").replace("\t","").strip()

                else :
                    keterangan = soup.find("span", class_="tv-screener__description").get_text().replace("/n","").replace("/t","").replace("\n","").replace("\t","").strip()

                last = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").get_text()
                chg_persen = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").get_text()
                chg = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").find_next("td").get_text()
                rating = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").find_next("td").find_next("td").get_text()
                # try:
                #     chg_persen = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big tv-screener-table__cell--up").get_text()
                #     try:
                #         chg = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big tv-screener-table__cell--up").find_next("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big tv-screener-table__cell--up").get_text()
                #     except:
                #         chg = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big tv-screener-table__cell--up").find_next("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--down tv-screener-table__cell--big tv-screener-table__cell--with-marker").get_text()
                # except :
                #     chg_persen = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--down tv-screener-table__cell--big tv-screener-table__cell--with-marker").get_text()
                #     try :
                #         chg = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--down tv-screener-table__cell--big tv-screener-table__cell--with-marker").find_next("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big tv-screener-table__cell--up").get_text()
                #     except:
                #         chg_persen = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--down tv-screener-table__cell--big tv-screener-table__cell--with-marker").find_next("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--down tv-screener-table__cell--big tv-screener-table__cell--with-marker").get_text()
                #
                # try :
                #     rating = soup.find("span", class_="tv-screener-table__signal tv-screener-table__signal--sell").get_text()
                # except:
                #     try:
                #         rating = soup.find("span", class_="tv-screener-table__signal tv-screener-table__signal--buy").get_text()
                #     except:
                #         try:
                #             rating = soup.find("span", class_="tv-screener-table__signal tv-screener-table__signal--neutral").get_text()
                #         except:
                #             rating = soup.find("span", class_="tv-screener-table__signal tv-screener-table__signal--strong-buy").get_text()

                vol = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").find_next("td").find_next("td").find_next("td").get_text()

                mkt_cap = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").get_text()

                pe = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").get_text()

                eps = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").get_text()

                employees = soup.find("td", class_="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").get_text()

                result = {
                    "company" : str(company),
                    "keterangan" : str(keterangan),
                    "last" : str(last),
                    "chg_%" : str(chg_persen),
                    "chg" : str(chg),
                    "rating" : str(rating),
                    "vol" : str(vol),
                    "mkt_cap" : str(mkt_cap),
                    "p/e" : str(pe),
                    "eps(ttm)" : str(eps),
                    "employees" : str(employees),
                    "date_crawl": crawl_date,
                    "url": url
                }
                # print(result)
                if "/" in category:
                    category = str(category).replace("/",", ")
                self.create_folder(crawl_date, main_category, category)

                with open("/home/" + self.website + "/" + crawl_date + "/" + main_category + "/" + category + "/" + company +".json", 'w') as outfile:
                    json.dump(result, outfile)
                    outfile.close()
                    self.a = self.a+1
                print("data :" + str(self.a))
                print("main_category :" + str(main_category))
                print("category :" + category )




Merits().get_items()