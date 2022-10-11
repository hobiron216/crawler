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
    def create_folder(self, crawl_date, category, sub_category):
        Path(self.path+ self.site_name + "/html/" + crawl_date + "/" + category + "/" + sub_category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path+ self.site_name + "/json/" + crawl_date + "/" + category + "/" + sub_category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def get_browser(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        chrome_options.headless = True # also works
        browser = webdriver.Chrome(options=chrome_options,  executable_path='/usr/local/bin/chromedriver')

        browser.maximize_window()
        return browser

    def __init__(self):
        self.base_link = "https://www.sinarharian.com.my/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5,6,7,8,9,10]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
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
        self.path = "/home/news/"
        self.site_name = "sinarharian"

    def get_items(self):
        browser = self.get_browser()
        category="berita"
        sub_categorys= ['nasional', 'politik', 'global', 'edisi', 'semasa', 'sukan', 'bisnes', 'pendapat', 'isu', 'wawancara']

        for sub_category in sub_categorys:
            if sub_category == 'nasional':
                url = "https://www.sinarharian.com.my/Nasional"
                self.get_link(category,sub_category, url, browser)
            elif sub_category == 'politik':
                url ="https://www.sinarharian.com.my/Politik"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'global':
                url ="https://www.sinarharian.com.my/Global"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'edisi':
                url ="https://www.sinarharian.com.my/Edisi"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'semasa':
                url ="https://www.sinarharian.com.my/Semasa"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'sukan':
                url ="https://www.sinarharian.com.my/Sukan"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'bisnes':
                url ="https://www.sinarharian.com.my/Bisnes"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'pendapat':
                url ="https://www.sinarharian.com.my/Pendapat"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'isu':
                url ="https://www.sinarharian.com.my/Isu"
                self.get_link(category, sub_category, url, browser)
            elif sub_category == 'wawancara':
                url ="https://www.sinarharian.com.my/Wawancara"
                self.get_link(category, sub_category, url, browser)
        browser.close()


    def get_link(self, category, sub_category, url, browser):
        browser.get(url)
        x = 0
        while True:
            try:
                x = x + 1
                if x > 130:
                    break
                browser.find_element_by_class_name("moreinLinkFull").click()

                time.sleep(1)
                print(x)
            except:
                continue

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll("div", class_="row spacewithborder")

        for div in divs:
            href = div.find("a").attrs.get("href")
            self.list_link.append(href)

        # print(self.list_link)
        self.parser(category, sub_category)
        del self.list_link[:]

    def parser(self, category, sub_category ):
        z=0
        for url in self.list_link :
            if z > 0:
                break

            print("url : " + url)
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
                    r = requests.get(url, timeout=20, proxies=self.proxies, headers=headers)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            r.encoding = 'utf-8'
            html = r.text

            soup = BeautifulSoup(html, "html.parser")

            title = soup.find("meta", property="og:title")['content']
            try:
                author = soup.find("meta", {"name": "author"}).attrs['content']
            except:
                author = "BERNAMA"
            contents = soup.find("div", class_="text articleContent").findAll("p")
            content = ""
            y=0
            for content21 in contents:

                if y > 0:
                    break
                content = content + content21.get_text().replace("AKAN MENYUSUL", "").replace("\n", "").replace('\"','"')
                y = y + 1

            ndate = soup.find("meta", {"name": "datePublished"}).attrs['content']
            ndate = ndate.split(" ")
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

            if bulan < 2:
                z = z + 1
                break
            if tahun != 2021:
                z = z + 1
                break
            if bulan == 3 or bulan == 2:

                if hari > 2:

                    if bulan > 2:
                        print("skip")
                        continue


                crawl_date = self.crawl_date()
                self.create_folder(crawl_date, category, sub_category)

                href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                path_html = self.path + self.site_name + "/html/" + crawl_date + "/" + category + "/" + sub_category + "/" + href21 + ".html"

                result = {

                    "title": title,
                    "ndate": ndate,
                    "category": category + "/" + sub_category,
                    "content" : content,
                    "author" : author,
                    "sitename": self.site_name,
                    "date_crawl": crawl_date,
                    "path_html": path_html,
                    "url": url

                }
                # print (result)
                self.a = self.a + 1
                with open(self.path + self.site_name + "/html/" + crawl_date + "/" + category + "/" + sub_category + "/" + href21 + ".html",'w', encoding='utf8') as outfile:
                        outfile.write(str(soup))
                with open(self.path + self.site_name + "/json/" + crawl_date + "/" + category + "/" + sub_category + "/" +  href21 + ".json",'w', encoding='utf8') as outfile:
                        json.dump(result, outfile, ensure_ascii=False)
                print("jumlah data: " + str(self.a))
                print("sub_category : " + sub_category)



                
        # message = "Engine : Bj News  \n" + "Data : " + str(self.a)
        # self.telegram_bot_sendtext(str(message))
        



BjNews().get_items()

