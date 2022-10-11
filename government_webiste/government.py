import hashlib
import json
import sys

import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
# import cloudscraper

import time
import random
import pandas as pd
import codecs
import urllib3
import os
urllib3.disable_warnings()

class Spider:
    def create_folder(self, category, path):
        Path(path +"/" + "html/" + category + "/").mkdir(parents=True,exist_ok=True)
        Path(path + "/" + "json/" + category + "/").mkdir(parents=True, exist_ok=True)


    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.a = 0
        self.random_sleep = [0.1, 0.2, 0.3]
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.proxies2 = {'https': 'https://pxuser:r@h@s!@2o2o@159.65.3.103:8252',
                         'http': 'http://pxuser:r@h@s!@2o2o@159.65.3.103:8252'}
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]


        self.list_link_check = []
        self.list_category = []
        self.link_error = []
        self.header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_ga=GA1.3.2083738933.1652841740; _gid=GA1.3.1608612544.1653361705; _gat=1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
        self.cookies =  {
    '_ga': 'GA1.3.2083738933.1652841740',
    '_gid': 'GA1.3.1608612544.1653361705',
    '_gat': '1',
}# self.scraper = cloudscraper.create_scraper(delay=5)

    def get_items(self):
        # df = pd.read_csv(r'E:\government linked website database.csv',sep='|')

        # df.close()

        df = pd.read_csv('/home/shahid/crawler/spider/government linked website database_v2.csv', sep='|', encoding='cp1252')
        # df = pd.read_csv(r'E:\government linked website database_v2.csv', sep='|', encoding='cp1252')
        data=[]

        # print(df['website_desc'])
        y=0
        # "https://www.audit.gov.my/", "https://www.rurallink.gov.my/",
        sisa = ['https://www.intanbk.intan.my/iportal/ms/', 'https://www.adamas.gov.my/en/', 'https://www.bless2.gov.my/', 'http://masjidnegara.gov.my/mn/', 'https://www.aelb.gov.my/newaelb/', 'https://jpt.mohe.gov.my/portal/index.php/ms/', 'https://www.prison.gov.my/ms/', 'https://www.span.gov.my/']
        z=0
        for index, df2 in df.iterrows():

            soup_check=""
            self.list_link = []
            self.list_link_check = []

            href=""

            # base_url = "https://www.kpwkm.gov.my/kpwkm/"
            website = df2['Website']

            base_url = df2['link']

            # if z==0:
            #     if base_url !="https://www.intanbk.intan.my/iportal/ms/":
            #         continue
            #     else:
            #         z=z+1


            if base_url!="http://www.ism.gov.my/en/":
                continue
            else:
                print(base_url)

                # sys.exit()

            # if ".org" in base_url:
            #     continue
            # if ".com" in base_url:
            #     continue
            # if ".edu" in base_url:
            #     continue
            # if ".gov" not in base_url:
            #     continue
            base_url = base_url.split("gov.my/")[0]
            base_url = base_url + "gov.my/"

            # base_url = base_url.split(".my/")[0]
            # base_url = base_url + ".my/"

            url = df2['link']
            path = "/dataph/government6_2/"+ website
            if not base_url:
                continue

            # base_url = "http://www.bless2.gov.my/"
            print(base_url)

            if base_url in self.list_link_check:
                continue
            y = y + 1
            # if y <= 1:
            #     continue
            if y > 1:
                sys.exit()
            self.list_link_check.append(base_url)
            b = 0
            while True:
                try:
                    b = b + 1
                    if b > 5:
                        break
                    r = requests.get(base_url, timeout=30, headers=self.header, verify=False  )
                    break
                except requests.exceptions.RequestException as e:
                    print(base_url)
                    continue
            if b > 5:
                self.link_error.append(base_url)
                continue
            # if r.status_code != 200:
            #     print(r.status_code)
            #     self.link_error.append(base_url)
            #     continue

            html = r.text
            # print(html)

            soup = BeautifulSoup(html, 'html.parser')
            # base_url = base_url.replace("gov.my/", "gov.my")


            category = ""




            divs = soup.find("body").find_all("a")

            if not divs:
                divs = soup.find_all("a")
            for div in divs:
                try :

                    href = div.attrs.get('href')

                    if href:

                        if "penerbitan1?" in href:
                            continue
                        if "lensa-foto" in href:
                            continue
                        if "kalendar" in href:
                            continue
                        if "rseventspro/week" in href:
                            continue
                        if "eventsbyweek" in href:
                            continue
                        if "faqs?p" in href:
                            continue
                        if "home?p" in href:
                            continue
                        if "/mfa-directory?" in href:
                            continue
                        if "eventsbyweek" in href:
                            continue
                        if "/mfa-directory?" in href:
                            continue
                        if "#sjextraslider" in href:
                            continue
                        if "iccaldate" in href:
                            continue
                        if "gallery" in href:
                            continue
                        if "eventsbyday" in href:
                            continue
                        if "calendar" in href:
                            continue
                        if href == "/" or href == "/l" or href == "#":
                            continue
                        if "jpg" in href or "png" in href:
                            continue
                        if "jpeg" in href:
                            continue
                        if "gif" in href or "png" in href:
                            continue
                        if "JPG" in href or "PNG" in href:
                            continue
                        if "tel:+" in href:
                            continue
                        if "pdf" in href:
                            continue
                        if "file" in href:
                            continue
                        if "download" in href:
                            continue
                        if "mp3" in href:
                            continue
                        if "mp4" in href:
                            continue
                        if "zip" in href:
                            continue
                        if "xls" in href:
                            continue
                        if "javascript:" in href:
                            continue
                        if "://" in href:
                            if base_url not in href:
                                continue

                        if base_url not in href :
                            if href[0] == "/":
                                href = href[1:]
                            if "http://" not in href:
                                href = base_url + href
                            if href not in self.list_link_check:
                                self.list_link.append(href)

                        else :
                            if href[0] == "/":
                                href = href[1:]
                            if href not in self.list_link_check:
                                self.list_link.append(href)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    continue
            # print(self.list_link)
            # sys.exit()
            if not self.list_link:
                self.link_error.append(base_url)
                continue

            if "://" in category:
                print("aw")
                continue
            self.create_folder(category, path)

            # if ".php" in base_url:
            #     with open(path + "index.php", 'w', encoding='utf8') as outfile:
            #         outfile.write(str(soup))
            # else:
            #     with open(path + "index.php", 'w', encoding='utf8') as outfile:
            #         outfile.write(str(soup))



            soup_check = ""
            for url in self.list_link:
                try :
                    time.sleep(random.choice(self.random_sleep))

                    if url in self.list_link_check:
                        continue

                    self.list_link_check.append(url)
                    b = 0
                    while True:
                        try:
                            b = b + 1
                            if b > 5:
                                break
                            r = requests.get(url, timeout=10, headers=self.header, verify=False)
                            break
                        except requests.exceptions.RequestException as e:
                            print(url)
                            continue
                    if b > 5:
                        continue
                    # if r.status_code!=200:
                    #     continue

                    html = r.text
                    soup = BeautifulSoup(html, 'html.parser')
                    if soup_check == soup.get_text():
                        print("svnjsnvjsn")

                        continue
                    else:
                        soup_check = soup.get_text()

                    last_string_url = url[-1]
                    url_split = url.split("/")

                    if last_string_url == "/":
                        nama_file = url_split[-2].strip()
                    else:
                        nama_file = url_split[-1].strip()

                    if "http://" in url:
                        base_url_replace = base_url.replace("https://", "http://")
                    else:
                        base_url_replace = base_url

                    category = url.replace(base_url_replace, "").replace(nama_file, "")
                    print(url)


                    if "://" in category:
                        continue

                    #parsing
                    try:

                        raw_title = soup.find("title")
                        title = raw_title.get_text()
                        raw_body = soup.find("body")
                        body = raw_body.get_text().strip()
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        continue



                    if "The specified URL cannot be found." in soup.get_text():
                        continue
                    if "Maaf, halaman ini tidak dapat dipaparkan" in soup.get_text():
                        continue
                    if "Oops" in body:
                        continue
                    if "This page is currently unavailable." in soup.get_text():
                        continue
                    if "Access forbidden!" in soup.get_text():
                        continue
                    if "Page Not found" in soup.get_text():
                        continue
                    if "Page not found" in soup.get_text():
                        continue
                    if "page not found" in soup.get_text():
                        continue
                    if "Page Not Found" in soup.get_text():
                        continue
                    if "Error 404" in soup.get_text():
                        continue
                    if "404 Not Found" in soup.get_text():
                        continue
                    if "404 Kategori tidak dijumpai" in soup.get_text():
                        continue
                    if "This Page Doesn't Seem To Exist." in soup.get_text():
                        continue


                    crawl_date = self.crawl_date()
                    if ".html" in nama_file:
                        raw_html = path + "/" + "html/" + category + "/" + nama_file
                    else:
                        raw_html = path + "/" + "html/" + category + "/" + nama_file + ".html"
                    id = url + "_" + title
                    id_hash = hashlib.md5(id.encode('utf-8')).hexdigest()
                    result = {
                        "_id": id_hash,
                        "title": title,
                        "body": body,
                        "raw_title": str(raw_title),
                        "raw_body": str(raw_body),
                        "raw_html": raw_html,
                        "crawl_date": crawl_date,
                        "sitename": website,
                        "url": url
                    }


                    self.create_folder(category,path)

                    with open(raw_html, 'w', encoding='utf8') as outfile:
                        outfile.write(str(soup))

                    with open(path + "/" + "json/" + category + "/" +  nama_file + ".json", 'w', encoding='utf8') as outfile:
                                json.dump(result, outfile, ensure_ascii=False)
                    try :
                        size = os.path.getsize(raw_html)
                        if size <= 12000:
                            continue
                    except:
                        pass
                    divs = soup.find("body").find_all("a")

                    if not divs:
                        divs = soup.find_all("a")
                    list_url = []
                    for div in divs:
                        try :
                            href = div.attrs.get('href')
                            if href:
                                if "penerbitan1?" in href:
                                    continue
                                if "lensa-foto" in href:
                                    continue
                                if "kalendar" in href:
                                    continue
                                if "rseventspro/week" in href:
                                    continue
                                if "eventsbyweek" in href:
                                    continue
                                if "faqs?p" in href:
                                    continue
                                if "home?p" in href:
                                    continue
                                if "/mfa-directory?" in href:
                                    continue
                                if "eventsbyweek" in href:
                                    continue
                                if "/mfa-directory?" in href:
                                    continue
                                if "#sjextraslider" in href:
                                    continue
                                if "gallery" in href:
                                    continue
                                if "iccaldate" in href:
                                    continue
                                if "eventsbyday" in href:
                                    continue
                                if "calendar" in href:
                                    continue
                                if href == "/" or href == "/l" or href == "#":
                                    continue
                                if "jpg" in href or "png" in href:
                                    continue
                                if "jpeg" in href:
                                    continue
                                if "gif" in href or "png" in href:
                                    continue
                                if "JPG" in href or "PNG" in href:
                                    continue
                                if "tel:+" in href:
                                    continue
                                if "pdf" in href:
                                    continue
                                if "file" in href:
                                    continue
                                if "download" in href:
                                    continue
                                if "mp3" in href:
                                    continue
                                if "mp4" in href:
                                    continue
                                if "zip" in href:
                                    continue
                                if "xls" in href:
                                    continue
                                if "javascript:" in href:
                                    continue
                                if "mailto:" in href:
                                    continue
                                if "://" in href:
                                    if base_url not in href:
                                        continue


                                if base_url not in href:
                                    if href[0] == "/":
                                        href = href[1:]
                                    if "http://" not in href:
                                        href = base_url + href
                                    if href not in self.list_link_check:
                                        list_url.append(href)


                                else:
                                    if href[0] == "/":
                                        href = href[1:]
                                    if href not in self.list_link_check:
                                        list_url.append(href)
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            continue
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    continue


                if list_url:
                    self.get_url_loop(list_url, nama_file, base_url, path,website)
                else:
                    continue

    def get_url_loop(self, list_url, nama_file21, base_url, path, website):
        a=0
        list_url2=[]
        soup_check=""
        # print(list_url)
        while True:
            c=0
            for url in list_url:
                try :
                    if url in self.list_link_check:
                        continue

                    self.list_link_check.append(url)
                    if "https://www.frim.gov.my/feed/atom/" in url:
                        print("vdvhdxvhvd")
                        continue
                    # print("detail_category : " + nama_file21)
                    print("move to url loop : " + url)
                    print("url error : " + str(self.link_error))

                    time.sleep(random.choice(self.random_sleep))
                    b = 0
                    while True:
                        try:
                            b=b+1
                            if b>5:
                                break
                            r = requests.get(url, timeout=10, headers=self.header, verify=False)
                            break
                        except requests.exceptions.RequestException as e:
                            print(url)
                            continue
                    if b>5:
                        continue

                    # if r.status_code!=200:
                    #     print(r.status_code)
                    #     continue
                    r.encoding = 'utf-8'
                    html = r.text
                    soup = BeautifulSoup(html, "html.parser")
                    if soup_check == soup.get_text():
                        c = c + 1
                        if c > 10:
                            print("soup check")
                            break
                        continue
                    else:
                        soup_check = soup.get_text()

                    print("save html")
                    last_string_url = url[-1]
                    url_split = url.split("/")

                    if last_string_url == "/":
                        nama_file = url_split[-2].strip()
                    else:
                        nama_file = url_split[-1].strip()

                    if "http://" in url:
                        base_url_replace = base_url.replace("https://", "http://")
                    else:
                        base_url_replace = base_url

                    category = url.replace(base_url_replace, "").replace(nama_file, "")

                    if "://" in category:
                        print("///aff")
                        continue

                    # parsing
                    try:
                        raw_title = soup.find("title")
                        title = raw_title.get_text()
                        raw_body = soup.find("body")
                        body = raw_body.get_text().strip()
                    except:
                        continue

                    if "The specified URL cannot be found." in soup.get_text():
                        continue
                    if "Maaf, halaman ini tidak dapat dipaparkan" in soup.get_text():
                        continue
                    if "Oops" in body:
                        continue
                    if "This page is currently unavailable." in soup.get_text():
                        continue
                    if "Access forbidden!" in soup.get_text():
                        continue
                    if "Page Not found" in soup.get_text():
                        continue
                    if "Page not found" in soup.get_text():
                        continue
                    if "page not found" in soup.get_text():
                        continue
                    if "Page Not Found" in soup.get_text():
                        continue
                    if "Error 404" in soup.get_text():
                        continue
                    if "404 Not Found" in soup.get_text():
                        continue
                    if "404 Kategori tidak dijumpai" in soup.get_text():
                        continue
                    if "This Page Doesn't Seem To Exist." in soup.get_text():
                        continue

                    crawl_date = self.crawl_date()
                    if ".html" in nama_file:
                        raw_html = path + "/" + "html/" + category + "/" + nama_file
                    else:
                        raw_html = path + "/" + "html/" + category + "/" + nama_file + ".html"
                    id = url + "_" + title
                    id_hash = hashlib.md5(id.encode('utf-8')).hexdigest()
                    result = {
                        "_id": id_hash,
                        "title": title,
                        "body": body,
                        "raw_title": str(raw_title),
                        "raw_body": str(raw_body),
                        "raw_html": raw_html,
                        "crawl_date": crawl_date,
                        "sitename": website,
                        "url": url
                    }

                    self.create_folder(category, path)
                    with open(raw_html, 'w', encoding='utf8') as outfile:
                        outfile.write(str(soup))

                    with open(path + "/" + "json/" + category + "/" +  nama_file + ".json", 'w', encoding='utf8') as outfile:
                                json.dump(result, outfile, ensure_ascii=False)

                    # with open("governmentcom.json", 'w', encoding='utf8') as outfile:
                    #     json.dump( self.list_link_check, outfile)

                    try:
                        size = os.path.getsize(raw_html)
                        if size <= 12000:
                            continue
                    except:
                        pass
                    print("crawl url")

                    divs = soup.find("body").find_all("a")

                    if not divs:
                        divs = soup.find_all("a")
                    # print(html)

                    for div in divs:
                        try :
                            href = div.attrs.get('href')
                            if href:
                                if "penerbitan1?" in href:
                                    continue
                                if "lensa-foto" in href:
                                    continue
                                if "kalendar" in href:
                                    continue
                                if "rseventspro/week" in href:
                                    continue
                                if "eventsbyweek" in href:
                                    continue
                                if "faqs?p" in href:
                                    continue
                                if "home?p" in href:
                                    continue
                                if "/mfa-directory?" in href:
                                    continue
                                if "faqs?p" in href:
                                    continue
                                if "home?p" in href:
                                    continue
                                if "eventsbyweek" in href:
                                    continue
                                if "jpeg" in href:
                                    continue
                                if "/mfa-directory?" in href:
                                    continue
                                if "#sjextraslider" in href:
                                    continue
                                if "iccaldate" in href:
                                    continue
                                if "gallery" in href:
                                    continue
                                if "eventsbyday" in href:
                                    continue
                                if "calendar" in href:
                                    continue
                                if href == "/" or href == "/l" or href == "#":
                                    continue
                                if "jpg" in href or "png" in href:
                                    continue
                                if "gif" in href or "png" in href:
                                    continue
                                if "JPG" in href or "PNG" in href:
                                    continue
                                if "tel:+" in href:
                                    continue
                                if "pdf" in href:
                                    continue
                                if "file" in href:
                                    continue
                                if "download" in href:
                                    continue
                                if "mp3" in href:
                                    continue
                                if "mp4" in href:
                                    continue
                                if "zip" in href:
                                    continue
                                if "javascript:" in href:
                                    continue
                                if "xls" in href:
                                    continue

                                if base_url not in href:
                                    if href[0] == "/":
                                        href = href[1:]
                                    if "http://" not in href:
                                        href = base_url + href
                                    if href not in self.list_link_check:
                                        list_url2.append(href)

                                else:
                                    if href[0] == "/":
                                        href = href[1:]

                                    if href not in self.list_link_check:
                                        list_url2.append(href)

                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            continue
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    continue

            a=a+1
            print(a)

            if list_url2:
                # print(list_url2)
                list_url.clear()
                for data in list_url2:
                    list_url.append(data)
                list_url2.clear()
                continue
            else:
                break



Spider().get_items()

# self.browser = webdriver.Firefox(firefox_profile=profile, options=options,  executable_path='/home/shahid/spider/geckodriver')  # , executable_path=r"C:\Users\muham\Documents\laptop kantor\TugasmasEliaEM\geckodriver.exe")#
# self.browser.maximize_window()
