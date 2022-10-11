import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import random
import time

class Ricebowl:

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

    def create_folder(self, crawl_date):
        Path("/dataph/loker/" + self.website + "/item/json/" + crawl_date).mkdir(parents=True, exist_ok=True)
        Path("/dataph/loker/" + self.website + "/content/html/" + crawl_date).mkdir(parents=True, exist_ok=True)
        Path("/dataph/loker/" + self.website + "/content/json/" + crawl_date).mkdir(parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.ricebowl.my/state/"
        self.website = "ricebowl"
        self.a = 0
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
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
        crawl_date = self.crawl_date()
        print ("====================================================" + crawl_date + "============================================================")
        self.create_folder(crawl_date)
        citys=["johor","kedah","kuala-lumpur","melaka","negeri-sembilan","pahang","perak","pulau-pinang","sabah","sarawak", "selangor","terengganu"]
        z=0
        for city in citys:
            z=z+1
            # if z<=4:
            #     continue
            time.sleep(random.choice(self.random_sleep))
            user_agent = random.shuffle(self.user_agents)
            headers = {
                'authority': 'www.ricebowl.my',
                'accept': 'application/json, text/plain, */*',
                'authorization': 'Bearer f4526791-df02-49d9-b26e-4fe8143736ab',
                'user-agent': user_agent,
                'content-type': 'application/json',
                'origin': 'https://www.ricebowl.my',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.ricebowl.my/state/johor',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': '__gads=ID=cd897c0c622ef15f-22d61cd1c0c400bf:T=1605524175:RT=1605524175:S=ALNI_MZxiKqJtO9ZhT1lmF8IgWhGa460bQ; _ga=GA1.2.1750618540.1605524180; _hjid=54253dd8-f9a8-40a1-8aba-d97b8aede8c9; G_ENABLED_IDPS=google; __tawkuuid=e::ricebowl.my::UI4zlGHV/ckpKfkYA5MPB2q4HfWg92sGK01sOZf2uFUl0n3wnNvhyOE/7DjcYKh0::2; @@=1; SL_C_23361dd035530_KEY=a21ad5bf98812dce0b463b36a91128a754696ed5; __cfduid=d88d67e92219c1817782bdb5e384200c91612328566; lang=en; __stdf=0; __stp={"visit":"returning","uuid":"06f813f4-1d45-4951-ad59-bced629daea5","ck":"3928087"}; app=%7B%22auth%22%3A%7B%22token%22%3A%22eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzOTI4MDg3Iiwicm9sZXMiOlsiUk9MRV9KT0JTRUVLRVIiXSwiaXNzIjoiaHR0cHM6XC9cL2FwaS5tYXVrZXJqYS5teSIsImV4cCI6MTY0Mzg0NjQwMCwidXNlciI6eyJlbWFpbF92ZXJpZmllZCI6Im5vIiwicGhvbmVfdmVyaWZpZWQiOiJ5ZXMiLCJ1c2VyX2lkIjoiMzkyODA4NyIsIm5hbWUiOiJzaGFoaWQiLCJiYW5uZWQiOmZhbHNlfX0.jDMD9UV0WQ9fR64gLVlPNlg9n3u5grkEQTPGRLKM2PI%22%7D%7D; ricebowl_token=%7B%22auth%22%3A%7B%22token%22%3A%22eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzOTI4MDg3Iiwicm9sZXMiOlsiUk9MRV9KT0JTRUVLRVIiXSwiaXNzIjoiaHR0cHM6XC9cL2FwaS5tYXVrZXJqYS5teSIsImV4cCI6MTY0Mzg0NjQwMCwidXNlciI6eyJlbWFpbF92ZXJpZmllZCI6Im5vIiwicGhvbmVfdmVyaWZpZWQiOiJ5ZXMiLCJ1c2VyX2lkIjoiMzkyODA4NyIsIm5hbWUiOiJzaGFoaWQiLCJiYW5uZWQiOmZhbHNlfX0.jDMD9UV0WQ9fR64gLVlPNlg9n3u5grkEQTPGRLKM2PI%22%7D%7D; _gid=GA1.2.1596041377.1613019322; _hjIncludedInPageviewSample=1; _hjTLDTest=1; _hjAbsoluteSessionInProgress=0; __stgeo="0"; __stbpnenable=1; refCode=; sid=s%3AL4cuQdciCrfjnvN-zHKTxJ035UGjv-8a.lrYpwnkOrExNeiMwodsZd4fhUxRmAyaIg5lLTTDSL%2BY; fillJobAlert=true; utm=%7B%22source%22%3A%22website%22%2C%22medium%22%3A%22search%22%7D; jobdetail=1; jobbanner=12; language=eyJpdiI6InJDbloyazdNTnFkaFNhUUN6RkhUeXc9PSIsInZhbHVlIjoiMFFWeHZGejdDdkF6OEdkK1pGWExcL2c9PSIsIm1hYyI6ImMzMjNhMjM1MzMxYWVmYjI4MzVhYWU1NzVmYTkyMWRkOGNjNTFkZDlkMTVlMjAyMjg1Y2FjODhhNTlhNDJkYWUifQ%3D%3D; jobViewCount=5; __sts={"sid":1613019322117,"tx":1613020292376,"url":"https%3A%2F%2Fwww.ricebowl.my%2Fstate%2Fjohor","pet":1613020292376,"set":1613019322117,"pUrl":"https%3A%2F%2Fwww.ricebowl.my%2Fjob%2F1533244-Public-Relations%3Futm_source%3Dwebsite%26utm_medium%3Dsearch","pPet":1613020281089,"pTx":1613020281089}; laravel_session=eyJpdiI6Imw1bmNiUGtkZW43blNsYmwyMTMyZUE9PSIsInZhbHVlIjoiUGh2RUpWd0xlU0QrNTFEYUhIZlk1UXVUeDA1dFJUWDVqQUZOVnNtQk9oeGxsUlN3OGV3QVRCRHNsQ05JSU8zNTc1U2hYXC9uWll3ejRSOGdBVElqUlhRPT0iLCJtYWMiOiI1OTAxOWVmM2ViY2M4Nzk1Nzg0ZTU5Njk4MDVhZTVlZjRhMzA3NWU3NTI4MDYwYTMzMWQ2YzkxMDhmOTYzODQyIn0%3D; TawkConnectionTime=0',
            }

            data = '{"platformId":1,"term":"*","from":0,"size":300,"jobType":[],"sort":"relevance","jobLocation":"%s","state":"","education":[],"lowerSalary":0,"country":"","app":"ricebowlprod","category_id":[],"category_parent":[],"accept_fresh_graduate":false,"fast_response":false,"hot_jobs":false,"urgentjobs":false,"company_id":0,"company":"","work_remotely":""}' % city
            while True:
                try:
                    response = requests.post('https://www.ricebowl.my/search/job/en/search', headers=headers, data=data, proxies=self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print("connection timeout")
                    continue
            r = response.text
            try :
                r_api = json.loads(r)
                r_data = r_api['hits']
            except:
                continue
            for data in r_data:
                title = data['jobTitle']
                title = title.replace(" ", "-")
                id = data['jobPostID']
                link = "https://www.ricebowl.my/job/" + str(id) + "-" + str(title) + "?utm_source=website&utm_medium=search"
                salary = data['salaryLabel']
                result = {
                    "link" : link,
                    "salary" : salary
                }
                self.list_link.append(result)
            link_item = 'https://www.ricebowl.my/state/' + city
            link_hash = hashlib.md5(link_item.encode('utf-8')).hexdigest().upper()
            print(len(self.list_link))

            with open('/dataph/loker/' + self.website + '/item/json/' + crawl_date + '/' + link_hash + '.json','w') as outfile:
                json.dump(r_api, outfile)
                outfile.close()
            self.parser(self.list_link, crawl_date, city)
            del self.list_link[:]

        message = "Engine : Ricebowl  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))
    def parser(self,list_link, crawl_date, city):
        for data in list_link:
            try :
                url = data['link']
                salary = data['salary']
                print("url : " + url)

                benefits= " "
                requirments=" "
                responsibilities=" "

                link31= url
                time.sleep(random.choice(self.random_sleep))
                user_agent = random.shuffle(self.user_agents)
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

                # print(link31)

                while True:
                    try:
                        r3= requests.get(link31,timeout=10,headers=headers) #proxies=self.proxies)
                        break
                    except requests.exceptions.RequestException as e:
                        print(e)
                        continue
                html3= r3.text
                soup3= BeautifulSoup(html3,"html.parser")

                link3 = hashlib.md5(link31.encode('utf-8')).hexdigest().upper()

                title = soup3.find("h1", class_="title is-6 mb-1")
                if title ==None :
                    price21 = False
                    continue
                else :
                    title=title.get_text()
                company=soup3.find("a", class_="is-hover-changed has-text-dark").get_text()
                type = soup3.find("span", class_="is-size-8").find_next("span", class_="is-size-8").get_text()
                location= soup3.find("span", class_="is-size-8").find_next("span", class_="is-size-8").find_next("span", class_="is-size-8").get_text()
                post_date= soup3.find("span", class_="is-size-8").find_next("span", class_="is-size-8").find_next("span",class_="is-size-8").find_next("div",class_="column is-5-desktop").get_text().replace('\n','')

                requirments= soup3.find("div", class_="requirement")#.get_text()
                responsibilities= soup3.find("div", class_="responsibilities")#.get_text()
                benefits= soup3.find("div", class_="benefit has-margin-bottom-10-mobile")#.get_text()

                if requirments==None :
                    requirments=" "
                else :
                    requirments = requirments.find_next("div", class_="job-detail-text").get_text()
                if responsibilities == None :
                    responsibilities=" "
                else :
                    responsibilities = responsibilities.find_next("div", class_="job-detail-text").get_text()
                if benefits==None :
                    benefits=" "
                else :
                    benefits=benefits.find_next("div", class_="job-detail-text").get_text()


                path_html="/dataph/loker/" + self.website + "/content/html/" + crawl_date + "/" + link3 + ".html"

                obj3 = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "post_date": post_date,
                    "salary" : salary,
                    "type":type,
                    "requirments":requirments,
                    "responsibilities":responsibilities,
                    "benefits":benefits,
                    "crawl_date":crawl_date,
                    "path_html":path_html,
                    "url": link31
                }
                self.result.append(obj3)
                self.a = self.a + 1
                print("jumlah data: " + str(self.a))
                print("city: " + city)
                # print(self.result)

                with open('/dataph/loker/' + self.website + '/content/html/' + crawl_date + '/' + link3 + '.html', 'w') as outfile:
                    outfile.write(str((soup3).encode('utf-8')))
                    outfile.close()
                with open('/dataph/loker/' + self.website + '/content/json/' + crawl_date + '/' + link3 + '.json','w') as outfile:
                    json.dump(self.result, outfile)
                    outfile.close()
                    self.result.clear()
                    del self.result[:]

            except Exception as e :
                print(e)
                self.result.clear()
                del self.result[:]
                continue

Ricebowl().get_items()
