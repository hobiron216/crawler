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

    def create_folder(self, crawl_date):
        Path("/home/medical/" + self.website + "/" + crawl_date).mkdir(parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://meritsmmc.moh.gov.my/search/registeredDoctor?"
        self.website = "merits"
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

        for i in range(9000,15847):
            time.sleep(random.choice(self.random_sleep))
            user_agent = random.shuffle(self.user_agents)
            headers = {
                'authority': 'meritsmmc.moh.gov.my',
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

            url=self.base_link + "page=" + str(i)
            while True:
              try:
                r= requests.get(url, headers=headers, timeout=50)
                break
              except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            html=r.text
            soup= BeautifulSoup(html,"html.parser")
            divs= soup.find("table", class_="table table-striped table-bordered table-hover table-md").find("tbody").findAll("tr")
            try :
              for div in divs:
                  href=div.find("a").attrs.get("onclick")
                  href=href.split("'")
                  self.list_link.append(href[1])
            except:
              print (i)
              continue
            self.parser(self.list_link, crawl_date, i)
            self.list_link.clear()
            del self.list_link[:]

    def parser(self, list_link, crawl_date, page):
        for url in list_link:
            try :
                print("url : " + url)
                time.sleep(random.choice(self.random_sleep))
                user_agent = random.shuffle(self.user_agents)
                headers = {
                    'authority': 'meritsmmc.moh.gov.my',
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
                while True :
                  try:
                    r= requests.get(url, headers=headers, timeout=50)
                    break
                  except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
                html = r.text
                soup = BeautifulSoup(html, "html.parser")
                full_name= soup.find("div", id="div-full-name").find("div", class_="col-sm-6").get_text().replace("\n","").replace("\t","").replace('"','').strip()
                qualification= soup.find("div", id="div-qualification").find("div", class_="col-sm-6").get_text().replace("\n","").replace("\t","").strip()
                graduated_of= soup.find("div", id="div-graduated-of").find("div", class_="col-sm-6").get_text().replace("\n","").replace("\t","").strip()
                provisional_registration_number= soup.find("div", id="div-provisional-registration-number").find("div", class_="col-sm-6").get_text().replace("\n","").replace("\t","").strip()
                date_of_provisional_registration= soup.find("div", id="div-date-of-provisional-registration").find("div", class_="col-sm-6").get_text().replace("\n","").replace("\t","").strip()
                full_registration_number= soup.find("div", id="div-full-registration-number").find("div", class_="col-sm-6").get_text().replace("\n","").replace("\t","").strip()
                date_of_full_registration= soup.find("div", id="div-date-of-full-registration").find("div", class_="col-sm-6").get_text().replace("\n","").replace("\t","").strip()

                tables =soup.find("table", class_="table table-striped table-bordered table-hover table-md").find("tbody").findAll("tr")
                apc=[]
                not_found=soup.find("td", class_="center")
                if not_found !=None:
                    no=""
                    apc_year=""
                    apc_no=""
                    place_of_practice_others=""
                    place_of_practice_principle=""
                else :
                    for table in tables:
                        no= table.find("td").get_text().strip()
                        apc_year=table.find("td").find_next("td").get_text().strip().strip()
                        apc_no = table.find("td").find_next("td").find_next("td").get_text().strip()
                        place_of_practice_principle= table.find("td").find_next("td").find_next("td").find_next("td").get_text().replace("\t","").replace("/n","").replace("/t","").replace("\n\n","")

                        # print(place_of_practice_principle)
                        place_of_practice_principle=re.sub(' +', ' ', place_of_practice_principle).replace("\n \n","\n").replace("\n","|").strip()
                        # place_of_practice_principle=place_of_practice_principle.split("|")
                        # place_of_practice_principle = "|"+ place_of_practice_principle[0].strip() + "|" + place_of_practice_principle[1].strip() + "|" + place_of_practice_principle[2].strip() + "|" + place_of_practice_principle[3].strip() + "|" + place_of_practice_principle[4].strip()

                        place_of_practice_others = table.find("td").find_next("td").find_next("td").find_next("td").find_next("td").get_text().replace("\t","").replace("/n","").replace("/t","").replace("\n\n","")
                        place_of_practice_others=re.sub(' +', ' ', place_of_practice_others).replace("\n \n","\n").replace("\n","|").strip()

                        result_apc=  {
                                "no" :str(no),
                                "apc_year" : str(apc_year),
                                "apc_no" : str(apc_no),
                                "place_of_practice_principle" : str(place_of_practice_principle),
                                "place_of_practice_others" : str(place_of_practice_others),
                            }
                        apc.append(result_apc)


                result={
                    "full_name" : str(full_name),
                    "qualification" : str(qualification),
                    "graduated_of" : str(graduated_of),
                    "provisional_registration_number" : str(provisional_registration_number),
                    "date_of_provisional_registration" : str(date_of_provisional_registration),
                    "full_registration_number" : str(full_registration_number),
                    "date_of_full_registration": str(date_of_full_registration),
                    "apc" : apc,
                    "date_crawl" : crawl_date,
                    "url" : url

                }
                file_name = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                # print(result)
                self.result.append(result)
                with open('/home/medical/merits/'+crawl_date+'/'+file_name+'.json','w') as outfile:
                    json.dump(self.result, outfile)
                    outfile.close()
                    self.result.clear()
                    del self.result[:]
                self.a = self.a + 1
                print("jumlah data: " + str(self.a))
                print("page: " + str(page))
            except Exception as e:
                print(e)
                continue


Merits().get_items()