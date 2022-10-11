import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout


import random
import time

class Jobstreet:

    def telegram_bot_sendtext(self,bot_message):
        global response
        bot_token = '1381123927:AAEQ169ZfG5qQMvPaNaFyt8zBJzyeZ-feXc'
        bot_chatID = '1008898421'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        while True:
            try:
                response = requests.get(send_text, timeout=10)
                break
            except requests.exceptions.RequestException as e:
                print("gagal kirim telegram")
                continue

        return response.json()

    def create_folder(self, crawl_date):
        Path("/dataph/loker/" + self.website + "/item/html/" + crawl_date).mkdir(parents=True, exist_ok=True)
        Path("/dataph/loker/" + self.website + "/content/html/" + crawl_date).mkdir(parents=True, exist_ok=True)
        Path("/dataph/loker/" + self.website + "/content/json/" + crawl_date).mkdir(parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.jobstreet.com.my/en/job-search/job-vacancy.php?createdAt=1d"
        self.website = "jobstreet"
        self.a = 0
        self.b = 0
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
        self.result = []

    def get_items(self):
        user_agent = random.choice(self.user_agents)
        headers = {
        'authority': 'www.jobstreet.com.my',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'cookie': 'ABTestID=3792cf41-9501-49b7-9c1d-2359635e1663; ABSSRP=1334; ABSSRPGroup=B; ABHPGroup=B; ABJDGroup=B; sol_id=4f9461c9-2be5-4938-87a6-4ea867b09bf6; sol_id_pre_stored=4f9461c9-2be5-4938-87a6-4ea867b09bf6; s_vi=[CS]v1|2FD921EE0515A9CC-400006FE3A05FE41[CE]; _ga=GA1.3.1745367177.1605518300; _hjid=745f1b1b-ee26-44c6-91ab-db799c572b1e; _fbp=fb.2.1605518302003.1130534721; intercom-id-o7zrfpg6=c547afa4-4bcc-4561-a7a1-fe76192cce68; _gcl_au=1.1.2095282732.1614070718; ABIdpLot=1921094162; s_fid=1F32BD5429223BC2-25B3EA1FB9815D82; __utma=80927368.1745367177.1605518300.1614073862.1614073862.1; __utmz=80927368.1614073862.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __cfduid=d81171be706d078d78c9f03463dbcc79e1615198801; _gid=GA1.3.185374768.1615198803; intercom-session-o7zrfpg6=; RecentSearch=%7B%22Keyword%22%3Anull%7D; sol_id=4f9461c9-2be5-4938-87a6-4ea867b09bf6; __cfruid=4581febb761a40ce98297bcd12bf02cc96913092-1615260978; _gat_UA-82223804-1=1; _hjIncludedInSessionSample=0; _hjTLDTest=1; _hjAbsoluteSessionInProgress=1; ins-storage-version=34; inslastVisitedUrlmy=https%3A%2F%2Fwww.jobstreet.com.my%2Fen%2Fjob-search%2Fjob-vacancy.php%3Fojs%3D6',
    }

        # params = (
        #     ('createdAt', '3d'),
        # )
        while True:
                try:
                    r=requests.get(self.base_link, headers=headers, timeout=5)
                    html = r.text
                    try :
                        soup = BeautifulSoup(html, "html.parser")
                        # divs = soup.find("span", class_="FYwKg _2Bz3E C6ZIU_0 _1_nER_0 _2DNlq_0 _29m7__0 _1PM5y_0").get_text().split("of")
                        # divs =divs[1].replace("jobs ", "").replace(",","")
                        total = soup.find("div", id="jobList").attrs.get("data-sol-meta")
                        json_total = json.loads(total)
                        batas = json_total['totalJobCount']
                        print(batas)
                        batas = int(batas) / 30
                        print(batas)
                    except Exception as e:
                        print(e)
                        print("wkwkwk")
                        continue
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue


        for z in range(1, int(batas + 2)):
            crawl_date = self.crawl_date()
            self.create_folder(crawl_date)
            # if z<54:
            #     continue
            print ("page : " + str(z))
            url=self.base_link +"&pg="+str(z)
            item = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            with open('/dataph/loker/' + self.website + '/item/html/' + crawl_date + '/' + item + '.html', 'w') as outfile:
                outfile.write(str((soup).encode('utf-8')))
                outfile.close()

            time.sleep(random.choice(self.random_sleep))
            user_agent = random.choice(self.user_agents)
            headers = {
                'authority': 'www.jobstreet.com.my',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': 'ABTestID=3792cf41-9501-49b7-9c1d-2359635e1663; ABSSRP=1334; ABSSRPGroup=B; ABHPGroup=B; ABJDGroup=B; sol_id=4f9461c9-2be5-4938-87a6-4ea867b09bf6; sol_id_pre_stored=4f9461c9-2be5-4938-87a6-4ea867b09bf6; s_vi=[CS]v1|2FD921EE0515A9CC-400006FE3A05FE41[CE]; _ga=GA1.3.1745367177.1605518300; _hjid=745f1b1b-ee26-44c6-91ab-db799c572b1e; _fbp=fb.2.1605518302003.1130534721; intercom-id-o7zrfpg6=c547afa4-4bcc-4561-a7a1-fe76192cce68; _gcl_au=1.1.2095282732.1614070718; ABIdpLot=1921094162; s_fid=1F32BD5429223BC2-25B3EA1FB9815D82; __utma=80927368.1745367177.1605518300.1614073862.1614073862.1; __utmz=80927368.1614073862.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __cfduid=d81171be706d078d78c9f03463dbcc79e1615198801; _gid=GA1.3.185374768.1615198803; intercom-session-o7zrfpg6=; RecentSearch=%7B%22Keyword%22%3Anull%7D; sol_id=4f9461c9-2be5-4938-87a6-4ea867b09bf6; __cfruid=4581febb761a40ce98297bcd12bf02cc96913092-1615260978; _hjIncludedInSessionSample=0; _hjTLDTest=1; _gat_UA-82223804-1=1; ins-storage-version=50; inslastVisitedUrlmy=https%3A%2F%2Fwww.jobstreet.com.my%2Fen%2Fjob%2Fhr-executive-4499900%3FjobId%3Djobstreet-my-job-4499900%26sectionRank%3D30%26token%3D0~f143596f-0a4f-4a0d-8b4c-74b68d86a50b%26fr%3DSRP%2520Job%2520Listing',
            }


            while True:
                try:
                    r = requests.get(url, headers=headers, timeout=10)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue
            print(url)
            html = r.text
            soup = BeautifulSoup(html, "html.parser")

            divs = soup.findAll("div", class_="sx2jih0 zcydq89e zcydq88e zcydq872 zcydq87e")


            for i, div in enumerate(divs):
                # print("wkwkwk")
                href=div.find("a", class_="_1hr6tkx5 _1hr6tkx8 _1hr6tkxb sx2jih0 sx2jihf zcydq8h").attrs.get('href')
                self.list_link.append(href)
            self.parser(self.list_link,crawl_date)
            # print(self.list_link)
            del self.list_link[:]
        message = "Engine : Jobstreet  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))
        print("jumlah data gagal: " + str(self.b))
    def parser(self,list_link, crawl_date):
        for url in list_link:
            # print("url : " + url )


            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            ea_no=" "
            years_of_exp=" "
            salary=" "
            description=" "
            benefit_others=" "
            specific_location=" "
            avg_proc_time=" "
            registration_no=" "
            company_size=" "
            industry=" "

            # time.sleep(random.choice(self.random_sleep))
            user_agent = random.choice(self.user_agents)
            headers = {
                'authority': 'www.jobstreet.com.my',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': 'ABTestID=3792cf41-9501-49b7-9c1d-2359635e1663; ABSSRP=1334; ABSSRPGroup=B; ABHPGroup=B; ABJDGroup=B; sol_id=4f9461c9-2be5-4938-87a6-4ea867b09bf6; sol_id_pre_stored=4f9461c9-2be5-4938-87a6-4ea867b09bf6; s_vi=[CS]v1|2FD921EE0515A9CC-400006FE3A05FE41[CE]; _ga=GA1.3.1745367177.1605518300; _hjid=745f1b1b-ee26-44c6-91ab-db799c572b1e; _fbp=fb.2.1605518302003.1130534721; intercom-id-o7zrfpg6=c547afa4-4bcc-4561-a7a1-fe76192cce68; _gcl_au=1.1.2095282732.1614070718; ABIdpLot=1921094162; s_fid=1F32BD5429223BC2-25B3EA1FB9815D82; __utma=80927368.1745367177.1605518300.1614073862.1614073862.1; __utmz=80927368.1614073862.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __cfduid=d81171be706d078d78c9f03463dbcc79e1615198801; _gid=GA1.3.185374768.1615198803; intercom-session-o7zrfpg6=; RecentSearch=%7B%22Keyword%22%3Anull%7D; sol_id=4f9461c9-2be5-4938-87a6-4ea867b09bf6; __cfruid=4581febb761a40ce98297bcd12bf02cc96913092-1615260978; _hjIncludedInSessionSample=0; _hjTLDTest=1; _gat_UA-82223804-1=1; ins-storage-version=50; inslastVisitedUrlmy=https%3A%2F%2Fwww.jobstreet.com.my%2Fen%2Fjob%2Fhr-executive-4499900%3FjobId%3Djobstreet-my-job-4499900%26sectionRank%3D30%26token%3D0~f143596f-0a4f-4a0d-8b4c-74b68d86a50b%26fr%3DSRP%2520Job%2520Listing',
            }

            p=0
            while True:
                try:
                    r = requests.get("https://www.jobstreet.com.my"+url, timeout=10, headers=headers)
                    html2 = r.text
                    soup2 = BeautifulSoup(html2, "html.parser")
                    description21 = soup2.find("h4", class_="sx2jih0 _18qlyvc0 _18qlyvch _1d0g9qk4 _18qlyvcs _18qlyvc1x")
                                                             


                    # FYwKg C6ZIU_0 _3nVJR_0 _2VCbC_0 _2DNlq_0 _1VMf3_0
                    if description21 == None:

                        # print("https://www.jobstreet.com.my" + url)
                        print("error deskripsi")
                        p=p+1
                        if p>3:
                            break

                        continue
                    else:
                        description21 = description21.get_text()
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue

            if p>3:
                break

            divs2= soup2.findAll("div",class_="sx2jih0 zcydq8r zcydq8p _16wtmva0 _16wtmva4")
                                               




            for j,div2 in enumerate(divs2):
                title = div2.find("h1", class_="sx2jih0 _18qlyvc0 _18qlyvch _1d0g9qk4 _18qlyvcp _18qlyvc1x").get_text().replace('\n', '')

                company = div2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc2 _1d0g9qk4 _18qlyvcb").get_text().replace('\n', '')

                location = div2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").get_text().replace('\n', '')
                                                      
                                                     
                salary21 = div2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").get_text().replace('\n', '')
                                                     
                post_date = div2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").get_text().replace('\n', '')
                if post_date == "Multiple work locations":
                    location = salary21
                    salary21= div2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span").get_text().replace('\n', '')
                    post_date=div2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca").find_next("span").find_next("span").get_text().replace('\n', '')

                if len(post_date)>30 or post_date=="Responsibilites :":
                    salary=" "
                    post_date=salary21
                else :
                    salary=salary21




            if description21=="Job Description" :
                description = soup2.find("h4", class_="sx2jih0 _18qlyvc0 _18qlyvch _1d0g9qk4 _18qlyvcs _18qlyvc1x").find_next("div").get_text()

                career_level = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").get_text().replace('\n', '')
                                                          
                                                          
                qualification = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").get_text().replace('\n', '')
                years_of_exp = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                if years_of_exp=="Years of Experience":
                    years_of_exp = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                    job_type = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                    job_specialization = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                    overview = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text()

                    registration_no21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                    if registration_no21=="Registration No." :
                        registration_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        ea_no21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        if (ea_no21=="EA No."):
                            ea_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            industry=      soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            avg_proc_time= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            benefit_others=" "

                        elif(ea_no21=="Company Size"):
                            ea_no==" "
                            company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            avg_proc_time21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                            if avg_proc_time21=="Average Processing Time" :
                                avg_proc_time = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                industry = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if benefit_others=="Benefits & Others" :
                                    benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if specific_location=="Specific Location":
                                        specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        specific_location=" "

                                elif benefit_others=="Specific Location":
                                    benefit_others=" "
                                    specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                else :
                                    benefit_others=" "
                                    specific_location = " "

                            else :
                                avg_proc_time = " "
                                industry= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if benefit_others=="Benefits & Others":
                                    benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    if specific_location=="Specific Location":
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        specific_location=" "
                                elif benefit_others=="Specific Location":
                                    benefit_others = " "
                                    specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                else :
                                    benefit_others = " "
                                    specific_location = " "
                    else :
                        registration_no= " "
                        ea_no=" "
                        specific_location=" "
                        company_size=" "
                        avg_proc_time=" "
                        industry= " "
                        benefit_others=" "

                else:
                    years_of_exp = ""

                    job_type = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                    job_specialization = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                    overview = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text()

                    registration_no21= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                    if registration_no21=="Registration No." :
                        registration_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        ea_no21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        if (ea_no21=="EA No."):
                            ea_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            industry=  soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            avg_proc_time= " "
                            benefit_others=" "
                            specific_location=" "

                        elif(ea_no21=="Company Size"):
                            ea_no==" "
                            company_size =    soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            avg_proc_time21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                            if avg_proc_time21=="Average Processing Time":
                                avg_proc_time = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                industry = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if benefit_others=="Benefits & Others" :
                                    benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    if specific_location=="Specific Location":
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        specific_location=" "
                                elif benefit_others=="Specific Location":
                                    benefit_others=" "
                                    specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                else :
                                    benefit_others=" "
                                    specific_location=" "
                            else :
                                avg_proc_time=" "
                                industry=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                benefit_others=  soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if benefit_others=="Benefits & Others" :
                                    benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if specific_location=="Specific Location":
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        specific_location=""
                                elif benefit_others=="Specific Location":
                                    benefit_others=" "
                                    specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                else :
                                    benefit_others=" "
                                    specific_location=" "
                    else :
                        registration_no= " "
                        ea_no=" "
                        specific_location=" "
                        company_size=" "
                        avg_proc_time=" "
                        industry= " "
                        benefit_others=" "
            else :
                description21=soup2.find("h4", class_="sx2jih0 _18qlyvc0 _18qlyvch _1d0g9qk4 _18qlyvcs _18qlyvc1x").find_next("h4",class_="sx2jih0 _18qlyvc0 _18qlyvch _1d0g9qk4 _18qlyvcs _18qlyvc1x").get_text()
                if description21 == "Job Description":
                    description=soup2.find("h4", class_="sx2jih0 _18qlyvc0 _18qlyvch _1d0g9qk4 _18qlyvcs _18qlyvc1x").find_next("h4").find_next("div").get_text()
                    career_level= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                                            #sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb
                                #soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").get_text().replace('\n', '')

                    qualification= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                #soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").get_text().replace('\n', '')

                    years_of_exp= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')


                    if years_of_exp=="Years of Experience":
                        years_of_exp = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        job_type = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        job_specialization = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        overview = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text()
                        registrastion_no21= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        if registrastion_no21=="Registration No." :
                            registration_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')


                            ea_no21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            if (ea_no21=="EA No."):
                                ea_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                industry=      soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                benefit_others=" "

                            elif(ea_no21=="Company Size"):
                                ea_no==" "
                                company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if avg_proc_time21=="Average Processing Time" :
                                    avg_proc_time = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    industry = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others" :
                                        benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                        if specific_location=="Specific Location":
                                            specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=" "

                                    elif benefit_others=="Specific Location":
                                        benefit_others=" "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    else :
                                        benefit_others=" "
                                        specific_location = " "

                                else :
                                    avg_proc_time = " "
                                    industry= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others":
                                        benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        if specific_location=="Specific Location":
                                            specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=" "
                                    elif benefit_others=="Specific Location":
                                        benefit_others = " "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        benefit_others = " "
                                        specific_location = " "
                        else :
                            registration_no= " "
                            ea_no=" "
                            specific_location=" "
                            company_size=" "
                            avg_proc_time=" "
                            industry= " "
                            benefit_others=" "

                    else:
                        years_of_exp = ""

                        job_type = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        job_specialization = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        overview = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text()
                        registrastion_no21= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        if registrastion_no21=="Registration No." :
                            registration_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            ea_no21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            if (ea_no21=="EA No."):
                                ea_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                industry=  soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time= " "
                                benefit_others=" "
                                specific_location=" "

                            elif(ea_no21=="Company Size"):
                                ea_no==" "
                                company_size =    soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if avg_proc_time21=="Average Processing Time":
                                    avg_proc_time = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    industry = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others" :
                                        benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        if specific_location=="Specific Location":
                                            specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=" "
                                    elif benefit_others=="Specific Location":
                                        benefit_others=" "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    else :
                                        benefit_others=" "
                                        specific_location=" "
                                else :
                                    avg_proc_time=" "
                                    industry=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    benefit_others=  soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others" :
                                        benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                        if specific_location=="Specific Location":
                                            specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=""
                                    elif benefit_others=="Specific Location":
                                        benefit_others=" "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        benefit_others=" "
                                        specific_location=" "
                        else :
                            registration_no= " "
                            ea_no=" "
                            specific_location=" "
                            company_size=" "
                            avg_proc_time=" "
                            industry= " "
                            benefit_others=" "


                else :
                    description=" "
                    career_level= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                #soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").get_text().replace('\n', '')

                    qualification= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                #soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").get_text().replace('\n', '')

                    years_of_exp= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                    if years_of_exp=="Years of Experience":
                        years_of_exp = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        job_type = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        job_specialization = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        overview = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text()
                        registrastion_no21= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        if registrastion_no21=="Registration No.":

                            registration_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            ea_no21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            if (ea_no21=="EA No."):
                                ea_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                industry=      soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                benefit_others=" "

                            elif(ea_no21=="Company Size"):
                                ea_no==" "
                                company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if avg_proc_time21=="Average Processing Time" :
                                    avg_proc_time = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    industry = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others" :
                                        benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                        if specific_location=="Specific Location":
                                            specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=" "

                                    elif benefit_others=="Specific Location":
                                        benefit_others=" "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    else :
                                        benefit_others=" "
                                        specific_location = " "

                                else :
                                    avg_proc_time = " "
                                    industry= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others":
                                        benefit_others=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        if specific_location=="Specific Location":
                                            specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=" "
                                    elif benefit_others=="Specific Location":
                                        benefit_others = " "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        benefit_others = " "
                                        specific_location = " "
                        else :
                            registration_no= " "
                            ea_no=" "
                            specific_location=" "
                            company_size=" "
                            avg_proc_time=" "
                            industry= " "
                            benefit_others=" "
                    else:
                        years_of_exp = ""

                        job_type = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        job_specialization = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                        overview = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text()
                        registrastion_no21= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                        if registrastion_no21=="Registration No.":

                            registration_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            ea_no21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                            if (ea_no21=="EA No."):
                                ea_no = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                industry=  soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                company_size = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time= " "
                                benefit_others=" "
                                specific_location=" "

                            elif(ea_no21=="Company Size"):
                                ea_no==" "
                                company_size =    soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                avg_proc_time21 = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                if avg_proc_time21=="Average Processing Time":
                                    avg_proc_time = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    industry = soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others" :
                                        benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        if specific_location=="Specific Location":
                                            specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=" "
                                    elif benefit_others=="Specific Location":
                                        benefit_others=" "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    else :
                                        benefit_others=" "
                                        specific_location=" "
                                else :
                                    avg_proc_time=" "
                                    industry=soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    benefit_others=  soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                    if benefit_others=="Benefits & Others" :
                                        benefit_others= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                                        if specific_location=="Specific Location":
                                            specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                        else :
                                            specific_location=""
                                    elif benefit_others=="Specific Location":
                                        benefit_others=" "
                                        specific_location= soup2.find("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _1d0g9qk4 _18qlyvcb").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')
                                    else :
                                        benefit_others=" "
                                        specific_location=" "

                        else :
                            registration_no= " "
                            ea_no=" "
                            specific_location=" "
                            company_size=" "
                            avg_proc_time=" "
                            industry= " "
                            benefit_others=" "

            path_html="/dataph/loker/" + self.website + "/content/html/" + crawl_date + "/" + href21 + ".html"

            if len(career_level) >30:
                print(career_level.encode('utf-8'))
                print(str(url).encode('utf-8'))
                self.b= self.b+1
                continue
            obj = {
            "title" : title,
            "company" : company,
            "location" : location,
            "salary" : salary,
            "post_date" : post_date,
            "description" : description,
            "career_level" : career_level,
            "qualification" : qualification,
            "years_of_exp" : years_of_exp,
            "job_type" : job_type,
            "job_specialization" : job_specialization,
            "overview" : overview,
            "registration_no": registration_no,
            "ea_no":ea_no,
            "specific_location":specific_location,
            "company_size":company_size,
            "avg_proc_time":avg_proc_time,
            "industry":industry,
            "benefit_others":benefit_others,
            "crawl_date" : crawl_date,
            "path_html" : path_html,
            "url" : url

            }
            self.result.append(obj)

            with open('/dataph/loker/' + self.website + '/content/html/' + crawl_date + '/' + href21 + '.html','w') as outfile:
                outfile.write(str((soup2).encode('utf-8')))
                outfile.close()
            with open('/dataph/loker/' + self.website + '/content/json/' + crawl_date + '/' + href21 + '.json','w') as outfile:
                json.dump(self.result, outfile)
                outfile.close()
            self.result.clear()
            del self.result[:]
            self.a = self.a + 1
            print("jumlah data: " + str(self.a))
            # print(result)

Jobstreet().get_items()
