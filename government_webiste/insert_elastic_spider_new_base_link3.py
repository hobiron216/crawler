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
import re

df = pd.read_csv('/home/shahid/crawler/spider/government linked website database_v2.csv', sep='|', encoding='cp1252')
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
            response = helpers.bulk(es, data, index=_index, doc_type="_doc", request_timeout=20)
            break
        except Exception as e:
            print(e)
            # time.sleep(1)
            continue
            logger.error(f"{self.bulk_insert.__name__} : {absolute_path}")

w=0
y=0
for index, df2 in df.iterrows():
    sitename = df2['Website']
    base_url2 = df2['link']

    # if base_url2 in data_old:
    #     continue
    y = y + 1
    if y <= 82:
        continue
    if y > 123:
        sys.exit()
    list_data=[]

    name_index = sitename.replace(" ","_").lower()
    _index = "my_govt-site_2022"
    # print(_index)

    # if base_url2!="https://www.rmp.gov.my/":
    #     continue

    for root, dirs, files in os.walk("/dataph/government2/" + sitename + "/json/"):
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
            if root[-1] != "/":
                root = root + "/"

            raw_html = root + file

            # print(raw_html)
            f = codecs.open(raw_html, 'r', encoding="utf-8")
            try :
                json_data = json.load(f)
            except:

                continue

            id_hash = json_data['_id']
            title = json_data['title']
            body = json_data['body']
            body = re.sub(r'\n', ' ', body)
            body = re.sub(' +', ' ', body).replace(r"\n"," ")
            raw_title = json_data['raw_title']
            raw_body = json_data['raw_body']
            raw_html = json_data ['raw_html']
            sitename = json_data ['sitename']
            url = json_data['url']

            # print(raw_html)

            if "government4" in raw_html:
                raw_html = raw_html.replace("government4", "government2")
            if "government3" in raw_html:
                raw_html = raw_html.replace("government3", "government2")
            if "government4" in raw_html:
                raw_html = raw_html.replace("government4", "government2")
            if "government5_2" in raw_html:
                    raw_html = raw_html.replace("government5_2", "government2")
            if "government5" in raw_html:
                raw_html = raw_html.replace("government5", "government2")

            if "government6" in raw_html:
                raw_html = raw_html.replace("government6", "government2")

            if "selenium2" in raw_html:
                raw_html = raw_html.replace("selenium2/", "")

            # print(raw_html)
            # sys.exit()
          

            base_url = url.split(".my/")[0] + ".my/"
            if ".com/" in base_url:
                base_url = base_url.split(".com/")[0] + ".com/"
            html = raw_body
            soup = BeautifulSoup(html, 'html.parser')
            divs = soup.findAll("span")
            text = ""
            for div in divs:
                text21 = str(div)
                text = text + text21 + "\n\n"
            divs = soup.findAll("p")
            for div in divs:
                text21 = str(div)
                text = text + text21 + "\n\n"
            divs = soup.findAll("td")
            for div in divs:
                text21 = str(div)
                text = text + text21 + "\n\n"
            divs = soup.findAll("h1")
            for div in divs:
                text21 = str(div)
                text = text + text21 + "\n\n"
            divs = soup.findAll("h2")
            for div in divs:
                text21 = str(div)
                text = text + text21 + "\n\n"
            divs = soup.findAll("h3")
            for div in divs:
                text21 = str(div)
                text = text + text21 + "\n\n"
            divs = soup.findAll("h4")
            for div in divs:
                text21 = str(div)
                text = text + text21 + "\n\n"

            try:
                print(url)
                print(base_url)
            except:
                pass
            # if url !="https://www.myeg.com.my/privacy-policy#privacy5":
            #     continue
            # sys.exit()
            # id = url + "_" + title
            # id_hash = hashlib.md5(id.encode('utf-8')).hexdigest()
            result = {
                "_id" :id_hash,
                "title" : title,
                "body" : body,
                "raw_title" : raw_title,
                "raw_body" : raw_body,
                "ner_body" : text,
                "raw_html" : raw_html,
                "crawl_date" : crawl_date,
                "sitename" : sitename,
                "url" : url,
                "base_url": base_url
            }

            list_data.append(result)
            # print(list_data)
            # sys.exit()

            bulk_insert(list_data, _index)
            list_data.clear()



