import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from requests.exceptions import Timeout
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class Elelong:
    def telegram_bot_sendtext(self, bot_message):
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

    def create_folder(self, crawl_date):
        Path("/dataph/" + self.website + "/json/" + crawl_date).mkdir(parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return crawl_date

    def __init__(self):
        self.base_link = "https://elelong.kehakiman.gov.my/BidderWeb/Home/Index"
        self.website = "elelong"
        self.a = 0
        self.proxies = {'https': 'https://ProXy:Rahas!@2020@139.59.105.3:53128',
                        'http': 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        self.random_sleep = [1, 2, 3, 4, 5]
        self.result = []

#         self.cookies = {
#             'ASP.NET_SessionId': 'tk1cwx4ccvarhamm4xdkhl4z',
#             '__RequestVerificationToken_L0JpZGRlcldlYg2': 'nWBUhlYAbWGxl32aAJn1Vh3zjQKBKH4Gb3siAxoAAUdD-ck94P1XNIy-NwiXgZMu9lvPnlUpXl681QqDP1U_ZrUjqUOTeIepWLnlNUe0-Rc1',
# }



        self.a=0
    def parser (self) :
        i=0
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")  # linux only
        chrome_options.add_argument("--headless")
        chrome_options.headless = True  # also works
        browser = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')

        browser.maximize_window()
        browser.get(self.base_link)
        cookies21 = browser.get_cookies()
        cookies = {c['name']: c['value'] for c in cookies21}

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        token = soup.find("input").attrs.get("value")
        browser.close()
        print(token)
        print(cookies)

        while True:
            i = i + 1
            a=self.a

            data = {
   '__RequestVerificationToken': token,
  'state': '0',
  'priceRange': '0',
  'landUsed': '0',
  'restrictionInInterest': '0',
  'tenure': '0',
  'auctionDate': '',
  'propertyAddress': '',
  'pageIndex': i,
  'pageSize': '20'
}

            user_agent = random.choice(self.user_agents)
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://elelong.kehakiman.gov.my',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://elelong.kehakiman.gov.my/BidderWeb/Home/Index',
                'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            }

            time.sleep(random.choice(self.random_sleep))
            while True:
                try:
                    response = requests.post('https://elelong.kehakiman.gov.my/BidderWeb/Home/SearchAuction', headers=headers, cookies=cookies, data=data,  timeout=30)
                    try :
                      r= json.loads(response.text)
                    except Exception as e:
                      print (e)
                      continue
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
                    

            
            for data_parser in r["auctions"]:
                crawl_date = self.crawl_date()
                self.create_folder(crawl_date)
                link_ori = "https://elelong.kehakiman.gov.my/BidderWeb/Home/Detail/" + str(data_parser["RowId"])
                dict1={'crawl_date' : crawl_date}
                dict2={'link_ori' : link_ori}
                for data21 in data_parser["Properties"]:
                    data21.update(dict1)
                    data21.update(dict2)
                    self.result.append(data21)

                link_ori_hash = hashlib.md5(link_ori.encode('utf-8')).hexdigest().upper()
                with open('/dataph/'+ self.website + '/json/' + crawl_date + '/' + link_ori_hash + '.json','w') as outfile:
                    json_str = json.dumps(self.result)
                    outfile.write(json_str)
                    outfile.close()
                    self.result.clear()
                    del self.result[:]
                self.a=self.a+1

            print("Data : " + str(self.a))
            print("Page : " + str(i))
            if a == self.a:
                break
        message = "Engine : Elelong  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))
Elelong().parser()