import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from selenium import webdriver
from pyvirtualdisplay import Display
import random
import time
from dateutil.parser import parse
from selenium import webdriver
from pyvirtualdisplay import Display
class BjNews:

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
    def create_folder(self, crawl_date, category):
        Path(self.path+"html/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.a = 0
        self.z = 0
        self.base_link="https://www.hmetro.com.my"
        self.site_name="hmetro"
        self.random_sleep= [1,2,3,4,5,6,7,8,9,10]
        self.proxies = {'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
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
        self.list_link = []
        self.path = "/home/news/hmetro/"
        self.except_json = []
        self.display = Display(visible=0, size=(1366, 768))
        self.display.start()

    def get_items(self):
        user_agent = random.choice(self.user_agents)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", firefox_profile=profile )
        categorys = ['wm', 'addin', 'rencana', 'sihat', 'xpresi', 'vroom', 'pks', 'agro', 'spektrum']
        for category in categorys:
            self.z = 0
            if category == 'wm':
                # continue
                url = "https://www.hmetro.com.my/"+ category + "?page="
                self.get_url(category,url, browser)
            elif category == 'addin':
                # continue
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)
            elif category == 'rencana':
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)
            elif category == 'sihat':
                # continue
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)
            elif category == 'xpresi':
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)
            elif category == 'vroom':
                # continue
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)
            elif category == 'pks':
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)
            elif category == 'agro':
                # continue
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)
            elif category == 'spektrum':
                url = "https://www.hmetro.com.my/" + category + "?page="
                self.get_url(category, url, browser)

            # elif category == 'mutakhir' :
            #     # continue
            #     url = "https://www.hmetro.com.my/" + category + "?page="
            #     self.get_url(category, url, browser)


        message = "Engine : hmetro \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))
        browser.close()
        self.display.stop()

        # with open("except.json",'w',encoding='utf_8_sig') as outfile:
        #     json.dump(self.except_json, outfile, ensure_ascii=False)

    def get_url(self, category, url, browser) :
        z=0
        for i in range(0, 21):
            if self.z>0:
                break
            url21 = url + str(i)
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date, category)



            print(url21)
            browser.get(url21)
            time.sleep(4)
            html = browser.page_source
            # while True:
            #     try:
            #         r = requests.get(url21, timeout=10, headers=headers)
            #         break
            #     except requests.exceptions.RequestException as e:
            #         print("connetion timeout")
            #         continue
            # r.encoding = 'utf-8'
            # html = r.text


            soup = BeautifulSoup(html, "html.parser")
            # print(html)
            divs = soup.findAll("div", class_="article-teaser")
            # print(divs)
            for div in divs:
                try:
                    link = div.find("a").attrs.get("href")
                    self.list_link.append(link)
                except:
                    pass

            # print(len(self.list_link))
            # print(self.list_link)

            self.parser(self.list_link, crawl_date, category, i, browser)
            del self.list_link[:]

        
    def parser(self,list_link, crawl_date, category, page, browser):
        z=0
        for url in list_link:
            try :
                if z>0:
                    break

                url = self.base_link  + url
                print("url : " + url)

                # while True:
                #     try:
                #         r = requests.get(url, timeout=20, proxies=self.proxies, headers=headers)
                #         break
                #     except requests.exceptions.RequestException as e:
                #         print("connetion timeout")
                #         continue
                # r.encoding = 'utf-8'
                # html = r.text
                browser.get(url)
                time.sleep(3)
                html = browser.page_source

                soup = BeautifulSoup(html, "html.parser")

                ndate = soup.find("meta", property="article:published_time")['content']

                ndate = ndate.split("T")
                ndate = ndate[0]

                ndate_cek = ndate.split("-")
                ndate = ndate.replace("-", "")
                print(ndate_cek)
                bulan = ndate_cek[1]
                bulan = int(bulan)
                hari = ndate_cek[2]
                hari = int(hari)
                tahun = ndate_cek[0]
                tahun = int(tahun)

                if bulan < 3:
                    self.z = self.z + 1
                    break
                if tahun != 2021:
                    self.z = self.z + 1
                    break
                if bulan == 3 or bulan == 4 or bulan == 5:
                    title = soup.find("span", class_="d-inline-block mr-1").get_text().strip()
                    try :
                        author = soup.find("meta", property="article:author")['content']
                    except:
                        author = ""
                    ndate = soup.find("meta", property="article:published_time")['content']
                    ndate = ndate.split("T")
                    ndate = ndate[0]
                    ndate = ndate.replace("-", "")
                    contents= soup.find("div", class_="field field-body").findAll("p")
                    content22 = ""
                    for content21 in contents:
                        content22 = content22 + content21.get_text().strip()

                    location21 = content22.split(": ")

                    location = location21[0].strip()
                    if "Ayisy Yusof" in location:
                        location = location.replace("Ayisy Yusof", "")
                    try:
                        content = location21[1].strip()
                    except:
                        location = ""

                        content = location21[0].strip()

                    if len(location) > 100:
                        location = ""
                        content = content22

                    href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                    path_html = self.path + "html/" + crawl_date + "/" + category + "/" + href21 + ".html"

                    result = {

                        "title": title,
                        "ndate": ndate,
                        "category": category,
                        "location": location,
                        "content" : content,
                        "author" : author,
                        "sitename": self.site_name,
                        "date_crawl": crawl_date,
                        "path_html": path_html,
                        "url": url

                    }
                    # print (result)
                    self.a = self.a + 1
                    with open(self.path+"html/" + crawl_date + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                            outfile.write(str(soup))
                    with open(self.path+"json/" + crawl_date + "/" + category + "/" + href21 + ".json",'w',encoding='utf_8_sig') as outfile:
                            json.dump(result, outfile, ensure_ascii=False)
                    print("jumlah data: " + str(self.a))
                    print("category : " + category)
                    print("page : " + str(page))
            except:
                continue

            

BjNews().get_items()

