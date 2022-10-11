import hashlib
import json
import sys

import requests
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
# import cloudscraper
from elasticsearch import Elasticsearch, helpers
import time
import random
import pandas as pd
import os
from bs4 import BeautifulSoup
import codecs

df = pd.read_csv('/home/shahid/crawler/spider/government linked website database.csv', sep='|')
today = date.today()
crawl_date = today.strftime("%Y%m%d")

es = Elasticsearch(
    [{'host': '192.168.114.152', 'port': 9200}],
    # _ip.split(", "),
    # sniff before doing anything
    sniff_on_start=True,
    # refresh nodes after a node fails to respond
    sniff_on_connection_fail=True,
    # and also every 60 seconds
    sniffer_timeout=100,
    http_auth=('esph_my', '3Smy2o2!')
)

def bulk_insert(data, _index):

    while True:
        try:
            response = helpers.bulk(es, data, index=_index, doc_type="_doc")
            break
        except Exception as e:
            print(e)
            # time.sleep(1)
            continue
            logger.error(f"{self.bulk_insert.__name__} : {absolute_path}")

edu = ['https://www.mpm.edu.my/' ]
my = ['https://marii.my/' , 'https://www.amanahraya.my/', 'https://www.cybersecurity.my/', 'https://www.mimos.my/', 'https://www.sirim.my/']
sele = ['https://www.myeg.com.my/', 'https://www.lppsa.gov.my/v3/my/', 'https://www.malaysia.gov.my/portal/index']
for index, df2 in df.iterrows():
    sitename = df2['Website']

    base_url = df2['link']

    if base_url not in sele:
        continue

    if base_url == "https://www.myeg.com.my/":
        print("1")


    elif base_url == "https://www.lppsa.gov.my/v3/my/":
        print(2)
        base_url= "https://www.lppsa.gov.my/"
    else:
        base_url = base_url.split("gov.my/")[0]
        base_url = base_url + "gov.my/"

    # .com
    # if ".com" not in base_url:
    #     continue
    # if ".com.my/" in base_url:
    #     base_url = base_url.split("com.my/")[0]
    #     base_url = base_url + "com.my/"
    # else:
    #     base_url = base_url.split("com/")[0]
    #     base_url = base_url + "com/"

    # # .edu
    # base_url = base_url.split("edu.my/")[0]
    # base_url = base_url + "edu.my/"
    #
    # if base_url not in edu:
    #     continue



    # if ".org.my/" in base_url:
    #     base_url = base_url.split("org.my/")[0]
    #     base_url = base_url + "org.my/"
    # else:
    #     base_url = base_url.split("org/")[0]
    #     base_url = base_url + "org/"
    # .org
    # if ".org" not in base_url:
    #     continue

    # .my aja
    # base_url = base_url.split("my/")[0]
    # base_url = base_url + "my/"
    #
    # if base_url not in my:
    #     continue


    list_data=[]
    # print(sitename)

    name_index = sitename.replace(" ","_").lower()
    _index = "my_govt-site_2022"
    # print(_index)


    for root, dirs, files in os.walk("/dataph/goverment_selenium/" + sitename + "/"):
        for file in files:

            if "http" in root:
                continue
            # if "#sjextraslider" in file:
            #     continue
            # if "iccaldate" in file:
            #     continue
            # if "gallery" in file:
            #     continue
            if file == "/" or file == "/l" or file == "#":
                continue
            if "jpg" in file or "png" in file:
                continue
            if "gif" in file or "png" in file:
                continue
            if "JPG" in file or "PNG" in file:
                continue
            if "tel:+" in file:
                continue
            if "pdf" in file:
                continue
            if "file" in file:
                continue
            if "download" in file:
                continue
            if "mp3" in file:
                continue
            if "mp4" in file:
                continue
            if "zip" in file:
                continue
            if "xls" in file:
                continue
            if "javascript:" in file:
                continue
            if "mailto:" in file:
                continue
            if root[-1] !="/":
                root = root + "/"

            raw_html = root + file
            size = os.path.getsize(raw_html)
            if size<=1200:
                continue


            f = codecs.open(raw_html, 'r', encoding="utf-8")
            html = f.read()

            # print(raw_html)
            soup = BeautifulSoup(html,'html.parser')
            raw_html = root.replace("goverment_selenium", "government") + file
            try :
                raw_title = soup.find("title")
                title = raw_title.get_text()
                raw_body = soup.find("body")
                body = raw_body.get_text()
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
            if "Error 404" in soup.get_text() :
                continue
            if "404 Not Found" in soup.get_text() :
                continue
            if "404 Kategori tidak dijumpai" in soup.get_text() :
                continue
            if "This Page Doesn't Seem To Exist." in soup.get_text() :
                continue


            try :
                url = soup.find("meta", property="og:url")['content']
            except:
                try:
                    url = base_url + file
                except Exception as e:
                    url = soup.find("base").attrs.get("href")


            print(url)
            # print(base_url)
            print(raw_html)
            id = url + "_" + title
            id_hash = hashlib.md5(id.encode('utf-8')).hexdigest()
            result = {
                "_id" :id_hash,
                "title" : title,
                "body" : body,
                "raw_title" : str(raw_title),
                "raw_body" : str(raw_body),
                "raw_html" : raw_html,
                "crawl_date" : crawl_date,
                "sitename" : sitename,
                "url" : url
            }

            list_data.append(result)


            bulk_insert(list_data, _index)
            list_data.clear()




            # sys.exit()