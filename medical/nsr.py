import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import random
import time
import re

class Nsr:
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
        Path("/home/medical/" + self.website + "/" + crawl_date).mkdir(parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://nsr.org.my/"
        self.website = "nsr"
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
        crawl_date = self.crawl_date()
        self.create_folder(crawl_date)

        for i in range(1,676):
            time.sleep(random.choice(self.random_sleep))
            user_agent = random.shuffle(self.user_agents)
            headers = {
                'authority': 'nsr.org.my',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': 'XSRF-TOKEN=eyJpdiI6InM4UEc2ZEJmWnQzdU8wMHdVY1Nmb0E9PSIsInZhbHVlIjoid3hvV0FreThBWGZ2eGx1Um5uYWQ2V3llcDUwMitnXC96UExDZWJtY1R2Vk5kV0p3UVZHSHQ2Q2tkYzFoKzlYNjUiLCJtYWMiOiI5OGVmYzA3ODFlZTY1YmY1NTEzMTM4MWFjNDZkOTI1YTg1Zjk3ZWU5YmZjYTgzYjFiOThhODdlZmY1ZmI0ZWNlIn0%3D; merits_session=eyJpdiI6IjQ1YnlWZTRYckpVNWZjNWErY01zd1E9PSIsInZhbHVlIjoiU1EzRmVOUExwYnVkdVlMaDNveWtuQlJiODVZZllsMkxsekV0blwvTjVwRGVRZFRJMWwrcXlCSGdUTEJpNjB5cG4iLCJtYWMiOiIzYjNiM2ZlM2VmYWYxYTM3MTk4YWJjYjk0Y2U4YmY5MjBmNDBhMGI1YTIzYWRmYmNiYjdhNTE1ZDU3Yjc4NzkxIn0%3D',
            }

            url=self.base_link + "list1pview.asp?page="+ str(i)
            r= requests.get(url, headers=headers)
            html=r.text
            soup= BeautifulSoup(html,"html.parser")
            divs= soup.find("table", class_="table table-bordered searchlist nobottommargin").findAll("tr")
            z=0
            for div in divs:
                z=z+1
                if z==1:
                    continue
                href=div.find("a").attrs.get("href")
                href= self.base_link + href

                self.list_link.append(href)
            self.parser(self.list_link, crawl_date, i)
            self.list_link.clear()
            del self.list_link[:]
            # print(self.list_link)

    def parser(self, list_link, crawl_date, page):
        for url in list_link:

                print("url : " + url)
                time.sleep(random.choice(self.random_sleep))
                user_agent = random.shuffle(self.user_agents)
                headers = {
                    'authority': 'nsr.org.my',
                    'upgrade-insecure-requests': '1',
                    'user-agent': user_agent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-US,en;q=0.9,id;q=0.8'
                }
                while True:
                    try:
                        r= requests.get(url, headers=headers, timeout=5)
                        break
                    except requests.exceptions.RequestException as e:
                        print(e)
                        continue
                # print("success")
                html = r.text
                soup = BeautifulSoup(html, "html.parser")
                nsr_no = soup.find("table", class_="table table-bordered").find("span").get_text()
                name = soup.find("tr", id="tr_nameIC").find("span").get_text()
                title = soup.find("tr", id="tr_title").find("span").get_text()
                gender = soup.find("tr", id="tr_gender").find("span").get_text()
                email = soup.find("tr", id="tr_email")#.get_text()
                if email == None:
                    email = ""
                else :
                    email=email.find("span").get_text()
                fields_of_practice = soup.find("tr", id="tr_specialty").find("span").get_text().replace("\t","").replace("\n","").replace("\r","").strip()

                clinical_practices= soup.findAll("table", class_="table table-bordered")
                a=0
                b= len(clinical_practices) - 2
                clinical_practice_list = []
                qualification_list = []
                specialist_degree_list = []
                for clinical_practice in clinical_practices:
                    a=a+1
                    if a==1:
                        continue

                    if a>b:
                        if a+1==len(clinical_practices):
                            continue
                        degrees = clinical_practice.findAll("tr")
                        c=0
                        d=0
                        for degree in degrees:

                            if "Basic" in degree.get_text() :
                                c=1
                                continue

                            if c==1 and "Specialist" not in degree.get_text():
                                basic_degree = degree
                                degree_membership_fellowship_basic= basic_degree.find("span", class_="display1").get_text().replace("\t","").replace("\n","").replace("\r","").strip()
                                awarding_body_basic = basic_degree.find("span", class_="display1").find_next("span", class_="display1").get_text().replace("\t","").replace("\n\n","").replace("\n \n","") .replace("\n","|").replace("\r","").strip()
                                awarding_body_basic = awarding_body_basic[1:-1].strip()
                                year_of_award_basic = basic_degree.find("span", class_="display1").find_next("span", class_="display1").find_next("span", class_="display1").get_text()

                                result_qualification=  {
                                        "degree_membership_fellowship" :str(degree_membership_fellowship_basic),
                                        "awarding_body" : str(awarding_body_basic),
                                        "year_of_award" : str(year_of_award_basic)
                                    }
                                qualification_list.append(result_qualification)
                            if "Specialist" in degree.get_text() :
                                c=0
                                d=1
                                continue
                            if d==1:
                                special_degree = degree
                                degree_membership_fellowship_special= special_degree.find("span", class_="display1").get_text().replace("\t","").replace("\n","").replace("\r","").strip()
                                awarding_body_special =  special_degree.find("span", class_="display1").find_next("span", class_="display1").get_text().replace("\t","").replace("\n\n","").replace("\n \n","") .replace("\n","|").replace("\r","").strip()
                                awarding_body_special = awarding_body_special[1:-1].strip()
                                year_of_award_special = special_degree.find("span", class_="display1").find_next("span", class_="display1").find_next("span", class_="display1").get_text()

                                result_specialist_degree=  {
                                        "degree_membership_fellowship" :str(degree_membership_fellowship_special),
                                        "awarding_body" : str(awarding_body_special),
                                        "year_of_award" : str(year_of_award_special)
                                    }
                                specialist_degree_list.append(result_specialist_degree)

                    else :
                        clinical_practice_name= clinical_practice.find("span").get_text().replace("\t","").replace("\n","").replace("\r","").strip()
                        clinical_practice_address= clinical_practice.find("span").find_next("span").get_text().replace("\t","").replace("\n","").replace("\r","").strip().encode("ascii", "ignore").decode("utf-8").strip()
                        clinical_practice_address = " ".join(clinical_practice_address.split())
                        clinical_practice_tel_no = clinical_practice.find("span").find_next("span").find_next("span").get_text()
                        clinical_practice_fax_no = clinical_practice.find("span").find_next("span").find_next("span").find_next("span").get_text()

                        result_clinical_practice=  {
                                "name" :str(clinical_practice_name),
                                "address" : str(clinical_practice_address),
                                "tel_no" : str(clinical_practice_tel_no),
                                "fax_no" : str(clinical_practice_fax_no)
                            }
                        clinical_practice_list.append(result_clinical_practice)

                result={
                    "nsr_no" : str(nsr_no),
                    "title" : str(title),
                    "name" : str(name),
                    "gender" : str(gender),
                    "email" : str(email),
                    "fields_of_practice" : str(fields_of_practice),
                    "clinical_practices" : clinical_practice_list,
                    "qualification" : {
                        "basic_degree" : qualification_list,
                        "specialist_degree" :specialist_degree_list
                        },
                    "date_crawl" : crawl_date,
                    "url" : url

                }
                # print(result)
                file_name = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                # # print(result)
                # self.result.append(result)
                with open('/home/medical/'+ self.website + '/' +  crawl_date +'/' +file_name+'22.json','w') as outfile:
                    json.dump(result, outfile)
                    outfile.close()
                    self.result.clear()
                    del self.result[:]
                self.a = self.a + 1
                print("jumlah data: " + str(self.a))
                print("page: " + str(page))



Nsr().get_items()