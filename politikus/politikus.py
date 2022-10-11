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

class Politikus:
    def create_folder(self, crawl_date):
        Path("/home/" + self.website + "/" + crawl_date).mkdir(parents=True, exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://politikus.sinarproject.org/"
        self.website = "politikus"
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
        self.random_sleep = [1, 2, 3]
        self.result=[]

    def post(self,soup):
        data = []
        all_posts21 = soup.find("table", class_="table-striped").findAll("tr")


        for all_post21 in all_posts21:
            all_posts = all_post21.findAll("td")
            i = 0
            if not all_posts:
                continue
            for all_post in all_posts:
                i=i+1
                if i ==1:
                    try:
                        post = all_post.get_text().strip()
                    except:
                        post = ""
                elif i ==2:
                    try:
                        label = all_post.get_text().strip()
                    except:
                        label = ""
                elif i ==3:
                    try:
                        role = all_post.get_text().strip()
                    except:
                        role = ""
                elif i ==4:
                    try:
                        organization = all_post.get_text().strip()
                    except:
                        organization = ""
                elif i ==5:
                    try :
                        on_behalf_of = all_post.get_text().strip()
                    except:
                        on_behalf_of = ""
                elif i ==6:
                    try:
                        start_date = all_post.get_text().strip()
                    except:
                        start_date = ""
                elif i ==7:
                    try :
                        end_date = all_post.get_text().strip()
                    except:
                        end_date = ""

            result = {
                "post" : post,
                "label" : label,
                "role" : role,
                "organization" : organization,
                "on_behalf_of" : on_behalf_of,
                "start_date" : start_date,
                "end_date" : end_date
            }
            data.append(result)

        return data
    def get_items(self):
        crawl_date = self.crawl_date()
        self.create_folder(crawl_date)
        user_agent = random.shuffle(self.user_agents)
        headers = {
            'authority': 'politikus.sinarproject.org',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://politikus.sinarproject.org/persons',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cookie': 'politikus=politikus-cookie1; _ga=GA1.2.1137815132.1634534518; _gid=GA1.2.949308673.1634534518; _gat_gtag_UA_29734766_16=1',
        }


        r = requests.get(self.base_link + "persons/@@faceted_query?version=53b1c4f5bd44bdf2ae8f0cb692286b83&b_start:int=0", headers=headers)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.find("li", class_="last").get_text().strip()

        for i in range(0,int(divs)):

            user_agent = random.shuffle(self.user_agents)
            headers = {
                'authority': 'politikus.sinarproject.org',
                'cache-control': 'max-age=0',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://politikus.sinarproject.org/persons',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': 'politikus=politikus-cookie1; _ga=GA1.2.1137815132.1634534518; _gid=GA1.2.949308673.1634534518; _gat_gtag_UA_29734766_16=1',
            }

            while True:
                try:
                    r = requests.get(self.base_link + "persons/@@faceted_query?version=53b1c4f5bd44bdf2ae8f0cb692286b83&b_start:int=" + str(i*10), headers=headers)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.findAll("div", class_="photoAlbumEntry")
            for div in divs:

                href = div.find("a").attrs.get("href")
                self.list_link.append(href)
            self.parser(self.list_link, crawl_date, i)
            self.list_link.clear()

    def parser(self, list_link, crawl_date, page):
        for url in list_link:
                # url = "https://politikus.sinarproject.org/persons/abdul-azeez-abdul-rahim"
                print("url : " + url)
                time.sleep(random.choice(self.random_sleep))
                user_agent = random.shuffle(self.user_agents)
                headers = {
                    'authority': 'politikus.sinarproject.org',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'upgrade-insecure-requests': '1',
                    'user-agent': user_agent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': 'https://politikus.sinarproject.org/persons',
                    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                    'cookie': 'politikus=politikus-cookie1; _ga=GA1.2.1137815132.1634534518; _gid=GA1.2.949308673.1634534518; _gat_gtag_UA_29734766_16=1',
                }
                while True:
                    try:
                        r= requests.get(url, headers=headers, timeout=5)
                        break
                    except requests.exceptions.RequestException as e:
                        print(e)
                        continue

                html = r.text
                soup = BeautifulSoup(html, "html.parser")

                gender = ""
                birthdate = ""
                nationalities = ""
                tax_residencies = ""
                description = ""
                politically_exposed_person = ""
                membership_and_posts =  ""
                family_relationships = ""
                business_and_other_relationships = ""
                biography = ""
                notes = ""
                pep_status_details = ""
                subitems =""
                ownership_statements = ""
                cited_on_issues = ""
                procurement = ""

                general_datas = soup.findAll("dt")
                i=0
                for general_data in general_datas:
                    i=i+1
                    if general_data.get_text() == "Gender":
                        gender = general_data.find_next("dd").get_text().strip()
                    elif general_data.get_text() == "Birthdate":
                        birthdate = general_data.find_next("dd").get_text().strip()
                    elif general_data.get_text() == "Nationalities":
                        nationalities = general_data.find_next("dd").get_text().strip()
                    elif general_data.get_text() == "Tax Residencies" :
                        tax_residencies = general_data.find_next("dd").get_text().strip()
                    elif general_data.get_text() == "Politically Exposed Person" :
                        politically_exposed_person = general_data.find_next("dd").get_text().strip()


                description = soup.find("p").get_text()
                try:
                    membership_and_posts = self.post(soup)
                except:
                    pass
                try:
                    family_relationships = soup.find("div", class_="col-md-5").get_text().replace("\n", "").replace("Family Relationships","").strip()
                except:
                    pass
                try:
                    business_and_other_relationships = soup.find("div", class_="col-md-5").find_next("div", class_="col-md-5").get_text().replace("\n","").replace("Business and other Relationships","").strip()
                except:
                    pass

                h4_datas = soup.findAll("h4")
                i=0
                for h4_data in h4_datas:
                    i=i+1
                    if i<=3:
                        continue

                    if "Biography" in h4_data.get_text() :
                        try:
                            biography = h4_data.find_next().get_text().replace("\n", "").strip()
                        except:
                            pass
                    elif "Notes" in h4_data.get_text():
                        try:
                            notes = h4_data.find_next().get_text() + h4_data.find_next("p").get_text() + h4_data.find_next("p").find_next("h4").get_text()  + h4_data.find_next("p").find_next("h4").find_next("p").get_text()
                            notes = notes.replace("\n", "").strip()
                        except:
                            pass
                    elif "PEP Status Details" in h4_data.get_text():
                        try:
                            pep_status_details = h4_data.find_next().get_text().replace("\n", "").strip()
                        except:
                            pass
                    elif "Subitems" in h4_data.get_text():
                        try:
                            subitems = h4_data.find_next().get_text().replace("\n", "").strip()
                        except:
                            pass

                        if subitems:
                            subitems = []
                            subitems.append(h4_data.find_next().get_text().replace("\n", "").strip())
                            z=0
                            while True:
                                try :
                                    z=z+1
                                    if z ==1:
                                        b= h4_data.find_next("ul").find_next("ul")
                                    else:
                                        b= b.find_next("ul")
                                    sub_get_text = b.get_text().replace("\n", "").strip()

                                    if ")" not in sub_get_text :
                                        break
                                    else:
                                        subitems.append(sub_get_text)

                                except:
                                    continue

                    elif "Ownership Statements" in h4_data.get_text():
                        try:
                            ownership_statements = soup.find("div", class_="ownership-statement").get_text().replace("\n", "").replace("Ownership Statements","").strip()
                            ownership_statements = ' '.join(ownership_statements.split())
                        except:
                            pass
                    elif "Procurement" in h4_data.get_text():
                        try:
                            procurement = h4_data.find_next().get_text().replace("\n", "").strip()
                        except:
                            pass


                    elif "Cited on Issues" in h4_data.get_text():
                        try:
                            cited_on_issues = soup.find("div", class_="issue-source").get_text().replace("\n", "").replace("Cited on Issues", "").strip()
                            cited_on_issues = ' '.join(cited_on_issues.split())
                        except:
                            pass
                    elif "Procurement" in h4_data.get_text():
                        try:
                            procurement = h4_data.find_next().get_text().replace("\n", "").strip()
                        except:
                            pass


                result={
                    "gender" : gender,
                    "birthdate" : birthdate,
                    "nationalities" : nationalities,
                    "tax_residencies" : tax_residencies,
                    "description" : description,
                    "politically_exposed_person" : politically_exposed_person,
                    "membership_and_posts" : membership_and_posts,
                    "family_relationships" : family_relationships,
                    "business_and_other_relationships" : business_and_other_relationships,
                    "biography" : biography,
                    "notes" : notes,
                    "pep_status_details" : pep_status_details,
                    "subitems" : subitems,
                    "ownership_statements" : ownership_statements,
                    "cited_on_issues" : cited_on_issues,
                    "procurement" : procurement,
                    "date_crawl" : crawl_date,
                    "url" : url

                }

                file_name = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                # # print(result)
                # self.result.append(result)
                with open('/home/'+ self.website + '/' +  crawl_date +'/' +file_name+'22.json','w') as outfile:
                    json.dump(result, outfile)
                    outfile.close()


                self.a = self.a + 1
                print("jumlah data: " + str(self.a))
                print("page: " + str(page))



Politikus().get_items()