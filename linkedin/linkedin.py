import hashlib
import json
import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.options import Options

import random
import time

class Linkedin:

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
        self.base_link = "https://www.linkedin.com/jobs/jobs-in-malaysia/?sortBy=DD&f_TP=1%2C2&position=1&pageNum=0"
        self.website = "linkedin"
        self.a = 0
        self.proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.list_link = []
        # self.display = Display(visible=0, size=(1366, 768))
        # self.display.start()


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

    def get_browser(self):

        user_agent = random.choice(self.user_agents)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)


        browser = webdriver.Firefox(firefox_profile=profile, executable_path="/usr/local/bin/geckodriver")# executable_path=r"D:\geckodriver.exe")
        browser.maximize_window()

        return browser

    def get_items(self):
        crawl_date = self.crawl_date()
        print ("====================================================" + crawl_date + "============================================================")
        self.create_folder(crawl_date)

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
        z=0
        while True:

            if z ==1000:
                z= z - 1
            if z ==999 or z>999:
                break
            print(z)
            url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=&location=Malaysia&locationId=&geoId=106808692&f_TPR=r2592000&position=1&pageNum=0&start="+str(z)
            while True:
                try:
                    r = requests.get(url, timeout=10, headers=headers)  # proxies=self.proxies)#
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue

            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            # item = hashlib.md5(url.encode('utf-8')).hexdigest().upper()

            # with open('/dataph/loker/' + self.website + '/item/html/' + crawl_date + '/' + item + '.html', 'w') as outfile:
            #     outfile.write(str((soup).encode('utf-8')))
            #     outfile.close()

            divs = soup.findAll("li")

            if not divs:
                print("wkwkwk")
                continue
            href = soup.find("a", class_="base-card__full-link").attrs.get('href')
                                          # base-card__full-link
            self.list_link.append(href)

            for i, div in enumerate(divs):
                try:
                    href = div.find("a").attrs.get('href')
                    self.list_link.append(href)
                except:
                    print("wkwkwk")
                    print(z)
                    continue


            z = z + 25
            # break


        print(len(self.list_link))
        self.parser(self.list_link,crawl_date)
        del self.list_link[:]
        message = "Engine : Linkedin  \n" + "Data : " + str(self.a)
        self.telegram_bot_sendtext(str(message))
    def parser(self,list_link, crawl_date):
        for url in list_link:

            print("url : " + url)

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
                    r = requests.get(url, timeout=10,  headers=headers)#proxies=self.proxies)#
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue
            # r.encoding = 'utf-8'


            html2 = r.text
            soup2 = BeautifulSoup(html2, "html.parser")
            divs2 = soup2.findAll("li", class_="description__job-criteria-item")

            d = 0
            for l, div2 in enumerate(divs2):
                d = d + 1
                if d == 1:
                    seniority_level = div2.find("span",class_="description__job-criteria-text description__job-criteria-text--criteria").get_text().replace('\n', '')

                    continue
                elif d == 2:
                    employment_type = div2.find("span",class_="description__job-criteria-text description__job-criteria-text--criteria").get_text().replace('\n', '')
                    continue
                elif d == 3:
                    job_function1 = div2.find("span",class_="description__job-criteria-text description__job-criteria-text--criteria").get_text().replace('\n', '')
                    job_function2 = div2.find("span",class_="description__job-criteria-text description__job-criteria-text--criteria").find_next("span").get_text().replace('\n', '')
                    job_function3 = div2.find("span",class_="description__job-criteria-text description__job-criteria-text--criteria").find_next("span").find_next("span").get_text().replace('\n', '')
                    job_function4 = div2.find("span",class_="description__job-criteria-text description__job-criteria-text--criteria").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                    continue
                elif d == 4:
                    industries1 = div2.find("span",class_="description__job-criteria-text description__job-criteria-text--criteria").get_text().replace('\n', '')
                    industries2 = div2.find("span", class_="description__job-criteria-text description__job-criteria-text--criteria").find_next("span").get_text().replace('\n', '')
                    industries3 = div2.find("span", class_="description__job-criteria-text description__job-criteria-text--criteria").find_next("span").find_next("span").get_text().replace('\n', '')
                    industries4 = div2.find("span", class_="description__job-criteria-text description__job-criteria-text--criteria").find_next("span").find_next("span").find_next("span").get_text().replace('\n', '')

                    if industries2 == "Aktifkan peringatan pekerjaan" or industries2 == "Aktifkan pemberitahuan pekerjaan" or industries2 == "Turn on job alerts":
                        industries = industries1
                    elif industries3 == "Aktifkan peringatan pekerjaan" or industries3 == "Aktifkan pemberitahuan pekerjaan" or industries3 == "Turn on job alerts":
                        industries = industries1 + ", " + industries2
                    elif industries4 == "Aktifkan peringatan pekerjaan" or industries4 == "Aktifkan pemberitahuan pekerjaan" or industries4 == "Turn on job alerts":
                        industries = industries1 + ", " + industries2 + ", " + industries3
                    else:
                        industries = industries1 + ", " + industries2 + ", " + industries3 + ", " + industries4

                    if job_function4 == industries4 and (job_function4 == "Aktifkan peringatan pekerjaan" or job_function4 == "Aktifkan pemberitahuan pekerjaan" or industries2 == "Turn on job alerts"):
                        job_function = job_function1 + ", " + job_function2 + ", " + job_function3
                    elif job_function4 == industries3:
                        job_function = job_function1 + ", " + job_function2 + ", " + job_function3
                    elif job_function4 == industries2:
                        job_function = job_function1 + ", " + job_function2 + ", " + job_function3
                    elif job_function4 == industries1:
                        job_function = job_function1 + ", " + job_function2 + ", " + job_function3

                    if job_function3 == industries4 and (job_function3 == "Aktifkan peringatan pekerjaan" or job_function3 == "Aktifkan pemberitahuan pekerjaan"):
                        job_function = job_function1 + ", " + job_function2
                    elif job_function3 == industries3:
                        job_function = job_function1 + ", " + job_function2
                    elif job_function3 == industries2:
                        job_function = job_function1 + ", " + job_function2
                    elif job_function3 == industries1:
                        job_function = job_function1 + ", " + job_function2

                    if job_function2 == industries4 and (job_function2 == "Aktifkan peringatan pekerjaan" or job_function2 == "Aktifkan pemberitahuan pekerjaan" or industries2 == "Turn on job alerts"):
                        job_function = job_function1
                    elif job_function2 == industries3:
                        job_function = job_function1
                    elif job_function2 == industries2:
                        job_function = job_function1
                    elif job_function2 == industries1:
                        job_function = job_function1

            title = soup2.find("h1", class_="topcard__title")
            if title == None:
                print("title none")
                continue
            else :
                title = title.get_text().replace('\n', '')

            company = soup2.find("span", class_="topcard__flavor").get_text().replace('\n', '')
            location = soup2.find("span", class_="topcard__flavor topcard__flavor--bullet")
            if location == None:
                print("location none")
                continue
            else:
                location = location.get_text().replace('\n', '')

            # try :
            #     post_date = soup2.find("span", class_="topcard__flavor--metadata posted-time-ago__text").get_text().replace('\n', '')  # .get_text().replace('\n', '')
            # except:
            #     try :
            #         post_date = soup2.find("span", class_="topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new").get_text().replace('\n', '')
            #
            #     except:
            #         print(user_agent)
            #         continue
            try :
                res = soup2.find('script', {'type':'application/ld+json'})
                # print(res)
                res = str(res).split(">")
                # print(res)
                res = res[1]
                res = res.split("<")[0]
                # print(res)
                res= json.loads(res)
                post_date = res['datePosted']
                ndate = post_date.split("T")
                ndate = ndate[0]
                post_date = ndate.replace("-","")
            except Exception as e:
                print(e)
                continue

            description = soup2.find("div", class_="show-more-less-html__markup").get_text()

            href21 = hashlib.md5(url.encode('utf-8')).hexdigest().upper()
            path_html = "/dataph/loker/" + self.website + "/content/html/" + crawl_date + "/" + href21 + ".html"


            try :
                obj = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "post_date": post_date,
                    "description": description,
                    "seniority_level": seniority_level,
                    "employment_type": employment_type,
                    "job_function": job_function,
                    "industries": industries,
                    "crawl_date": crawl_date,
                    "path_html": path_html,
                    "url": url

                }
            except Exception as e:
                print(e)
                continue
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

Linkedin().get_items()
