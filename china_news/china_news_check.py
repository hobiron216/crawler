import hashlib
import json
import requests
from pathlib import Path
from logger import Logger
from datetime import  date, datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from selenium import webdriver
from pyvirtualdisplay import Display
from seleniumwire import webdriver
import random
import time
class Cn_News:

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
        Path(self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(self.path+"json/" + crawl_date + "/" + self.current_time + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def trim_word(self,word, from_start=0, from_end=0):
        return word[from_start:len(word) - from_end]

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://www.chinanews.com/"
        self.a = 0
        self.random_sleep= [1,2,3,4,5,6]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.proxies2 = {'https': 'https://pxuser:r@h@s!@2o2o@159.65.3.103:8252',
                         'http': 'http://pxuser:r@h@s!@2o2o@159.65.3.103:8252'}
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
        self.list_link2 = []
        self.display = Display(visible=0, size=(1366, 768))
        self.display.start()
        self.path = "/news_cn/requests/news/china_news/"

    def get_browser(self):
        options = {
	'proxy': {
   		 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128',
    		 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128',
    		 'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
    		}
}
        user_agent = random.choice(self.user_agents)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)

        browser = webdriver.Firefox(seleniumwire_options=options, firefox_profile=profile, executable_path='/usr/local/bin/geckodriver')
        #browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', seleniumwire_options=options)
        browser.maximize_window()
        
        return browser

    def get_items(self):
        with open(self.path + "/cek_url.json", 'r', encoding='utf_8_sig') as outfile:
            self.list_url= json.load(outfile)
        browser = self.get_browser()
        categorys = ['scroll-news', 'china', 'world', 'society', 'finance', 'business', 'fortune','auto', 'gangao', 'taiwan' , 'huaren', 'ent', 'sports', 'cul']
        crawl_date = self.crawl_date()
        today_time = datetime.today()
        self.current_time = today_time.strftime("%H")
        print ("====================================================" + crawl_date + "============================================================")
        for category in categorys:
            if category == 'scroll-news' :
                url= self.base_link + category
                self.get_html_soup(category, url)

            else :
                crawl_date = self.crawl_date()
                url=self.base_link + category
                self.create_folder(crawl_date, category)
                while True:
                    try :
                        browser.get(url)
                        break
                    except Exception as e:
                        print(e)
                        continue
                page="click scroll"
                z=0
                time.sleep(random.choice(self.random_sleep))
                
                while True:
                    try:
                        browser.find_element_by_id("page_bar0").click()
                        z=z+1
                        if z>5:
                            break
                        #time.sleep(1)
                    except:
                        break
                html=browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                divs = soup.findAll("div", class_="bigpic_list")
                for div in divs:
                    href=div.find("a").attrs.get("href")
                    if "chinanews.com" not in href:
                        href = "http://www.chinanews.com.cn" + href
                    if "http" not in href:
                        href = "http:" + href

                    self.list_link.append(href)
                self.parser(self.list_link,crawl_date,category,page)
                del self.list_link[:]
        browser.close()
        self.display.stop()

        with open(self.path + "/cek_url.json", 'w', encoding='utf_8_sig') as outfile:
            json.dump(self.list_url, outfile, ensure_ascii=False)

    def parser(self,list_link, crawl_date, category, page):
        for url in list_link:
            if url not in self.list_url:
                self.list_url.append(url)
            
                print("url : " + url)
                b = True
                # if len(url)<45:
                #     continue
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
                if "tp/hd" in url or "shipin" in url:
                    continue
                z = 0
                while b:
                    z = z + 1
                    try:
                        if z > 3:
                            b=False
                            break
                        r = requests.get(url, timeout=50, headers=headers)
                        b = False
                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        print(url)
                        continue
                r.encoding = 'utf-8'
                html = r.text

                soup = BeautifulSoup(html, "html.parser")
                title= soup.find("h1", attrs={"style":"display:block; position:relative; clear:both"}).get_text()
                article = soup.find("div", class_="left_zw").get_text()
                ndate = soup.find("div", class_="left-t").get_text().split("来")#split
                ndate =ndate[0]

                href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                path_html = self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html"

                result = {

                    "title": title,
                    "article": article,
                    "ndate": ndate,
                    "category": category,
                    "crawl_date": crawl_date,
                    "path_html": path_html,
                    "url": url

                }
                # print (result)
                self.a = self.a + 1
                with open(self.path+"html/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".html",'w',encoding='utf8') as outfile:
                    outfile.write(str(soup))
                with open(self.path+"json/" + crawl_date + "/" + self.current_time + "/" + category + "/" + href21 + ".json",'w',encoding='utf8') as outfile:
                    outfile.write(str(result))
                print("jumlah data: " + str(self.a))
                print("category : " + category)
                print("page : " + str(page))
                self.list_link2.append(url)
            
            

    def get_html_soup(self,category,url):
        crawl_date=self.crawl_date()
        self.create_folder(crawl_date, category)
        page = "num-page"
        for j in range(1,6):#1,6
            url21 = url + "/news" + str(j) + ".html"
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
                        r = requests.get(url21, timeout=50,  headers=headers)
                        break
                    except requests.exceptions.RequestException as e:
                        print("connetion html_soup timeout")
                        continue
            html=r.text
            soup=BeautifulSoup(html,'html.parser')
            divs=soup.find_all("div", class_="dd_bt")

            a=0
            for i,div in enumerate(divs):
                a=a+1
                href = div.find("a").attrs.get('href')
                if "chinanews.com" not in href:
                    href = "http://www.chinanews.com.cn" + href
                if "http" not in href:
                    href = "http:" + href
                self.list_link.append(href)
            #print(self.list_link)
            

        self.parser(self.list_link,crawl_date,category,page)
        del self.list_link[:]



Cn_News().get_items()
