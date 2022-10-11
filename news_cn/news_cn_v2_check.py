import hashlib
import json
import requests
from pathlib import Path
# from logger import Logger
from datetime import  date, datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import random
import time
import newspaper
class News_Cn:
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

    def __init__(self):
        # self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "http://news.cn/"
        self.a = 0
        self.random_sleep= [1,2]
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
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
        self.path = "/news_cn/requests/news/news_cn/"

    def get_items(self):
        with open(self.path + "/cek_url.json", 'r', encoding='utf_8_sig') as outfile:
            self.list_url= json.load(outfile)
        categorys = ['politic', 'international', 'finance', 'military', 'theory', 'opinion', 'law', 'hr', 'corruption', 'local', 'hong-kong_macau', 'taiwan' ]
        crawl_date = self.crawl_date()
        today_time = datetime.today()
        self.current_time = today_time.strftime("%H")
        print ("====================================================" + crawl_date + "============================================================")
        for category in categorys:
            if category == 'politic' :
                # continue
                category_link="politicspro"
                self.get_api_v1(category,category_link)
            elif category == 'international' :
                # continue
                category_link="worldpro"
                self.get_api_v1(category,category_link)
            elif category == 'finance' :
                # continue
                category_link="fortunepro"
                self.get_api_v1(category,category_link)
                # break
            elif category == 'military' :
                # continue
                self.get_html_newspaper3k(category)
            elif category == 'theory' :
                # continue
                nid="114435"
                self.get_api_v2(category,nid)
            elif category == 'opinion' :
                # continue
                nid="11228286"
                self.get_api_v2(category,nid)
            elif category == 'law' :
                # continue
                nid="11227928"
                self.get_api_v2(category,nid)
            elif category == 'hr' :
                # continue
                nid="11230270"
                self.get_api_v2(category,nid)
            elif category == 'corruption' :
                # continue
                nid="11230846"
                self.get_api_v2(category,nid)
            elif category == 'local' :
                # continue
                nid="11227970"
                self.get_api_v2(category,nid)
            elif category == 'hong-kong_macau' :
                # continue
                nid="11228405"
                self.get_api_v2(category,nid)
            elif category == 'taiwan' :
                # continue
                nid="11228415"
                self.get_api_v2(category,nid)

        with open(self.path + "/cek_url.json", 'w', encoding='utf_8_sig') as outfile:
            json.dump(self.list_url, outfile, ensure_ascii=False)

    def get_api_v1(self,category,category_link):
        page=0
        url= self.base_link + category_link + "/json/xh_"+category_link+"Depth.js"
        print (url)
        crawl_date = self.crawl_date()
        self.create_folder(crawl_date, category)
        time.sleep(random.choice(self.random_sleep))
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
                r=requests.get(url, timeout=50,  proxies=self.proxies, headers = headers)
                try :
                    r = r.text
                    r = r.split('Depth =')
                    r = r[1]
                    r = json.loads(r)
                except Exception as e:
                    print(e)
                    continue
                break
            except requests.exceptions.RequestException as e:
                print("connetion api timeout")
                continue


        datas=r['data']['list']
        for data in datas:
            link= data['artDetails'][0]['url']
            self.list_link.append(link)
        self.parser(self.list_link,crawl_date,category)
        del self.list_link[:]

    def get_api_v2(self,category,nid):
        page=100 #100
        url ="http://qc.wa.news.cn/nodeart/list?nid="+nid+"&pgnum=1&cnt="+str(page)+"&tp=1&orderby=1?callback=jQuery11240581078843432933_1603256936706&_=1603256936707"
        print(url)
        crawl_date = self.crawl_date()
        self.create_folder(crawl_date, category)
        time.sleep(random.choice(self.random_sleep))
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
                r=requests.get(url, timeout=50,  proxies=self.proxies, headers = headers)
                r = r.text
                r1 = self.trim_word(r, 41, 1)
                try :
                    r1 = json.loads(r1)
                except:
                    r1=r.text
                    r1= json.loads(r1)
                break
            except requests.exceptions.RequestException as e:
                print("connetion api timeout")
                continue



        for links in r1['data']['list']:
            link=links['LinkUrl']
            self.list_link.append(link)

        self.parser(self.list_link,crawl_date,category)
        del self.list_link[:]

    def get_html_newspaper3k(self,category):

        crawl_date = self.crawl_date()
        self.create_folder(crawl_date, category)
        url = "http://www.news.cn/milpro/"
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
                r = requests.get(url, timeout=50, proxies=self.proxies, headers=headers)
                break
            except requests.exceptions.RequestException as e:
                print("connetion timeout")
                continue

        r.encoding = 'utf-8'
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        divs = soup.find("div", class_="contener")
        divs1 = divs.findAll("a")
        for div in divs1:
            link=div.attrs.get('href')
            if "mil" in link:
                # print(link)
                self.list_link.append(link)
        self.parser(self.list_link,crawl_date,category)
        del self.list_link[:]


    def parser(self,list_link, crawl_date, category):
        for url in list_link:
            url=str(url)
            if url not in self.list_url:
                self.list_url.append(url)
                print("url : " + url)
                b = True
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
                i=0
                while b:
                    try:
                        i=i+1
                        if i>=5:
                            b= False
                        r = requests.get(url, timeout=50, proxies=self.proxies, headers=headers)
                        try :
                            r.encoding = 'utf-8'
                        except:
                            continue
                        b = False

                    except requests.exceptions.RequestException as e:
                        print("connetion timeout")
                        continue

                html = r.text
                soup = BeautifulSoup(html, "html.parser")
                try :
                    title = soup.find("span", class_="title")
                    if title == None:
                        title = soup.find("div", class_="h-title").get_text()
                    else :
                        title=title.get_text()
                    # if title == None:
                    #     continue
                    # else:
                    #     title=title.get_text()
                    article = soup.find("div", id="detail").get_text()
                    year = soup.find("span", class_="year").get_text().replace("\n", "").replace(" ", "")
                    day21 = soup.find("span", class_="day").get_text().replace(" ", "")
                    day21 = day21.split("/")

                    try:
                        month = day21[0]
                        day = day21[1]
                        time21 = soup.find("span", class_="time").get_text().replace(" ", "")
                        ndate = year + "-" + month + "-" + day + " " + time21
                    except:
                        month = day21[0].replace("\r\n", "")
                        day = day21[1].replace("\r\n", "")
                        ndate = year + "-" + month + "-" + day + " " + "12:00:01"

                except Exception as e:
                    print(e)
                    continue

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
                self.list_link2.append(url)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date


News_Cn().get_items()

