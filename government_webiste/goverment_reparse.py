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
list_data =[]
for index, df2 in df.iterrows():
    sitename = df2['Website']
    base_url2 = df2['link']

    for root, dirs, files in os.walk("/dataph/government2/" + sitename + "/json/"):
        for file in files:

            raw_html = root + file
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

            base_url = url.split(".my/")[0] + ".my/"
            if ".com/" in base_url:
                base_url = base_url.split(".com/")[0] + ".com/"

            soup = BeautifulSoup(raw_body,'html.parser')
            new_body = soup.find("p").get_text()
            print(new_body)
            print(base_url)
            sys.exit()
            result = {
                "_id" :id_hash,
                "title" : title,
                # "body" : body,
                "raw_title" : raw_title,
                # "raw_body" : raw_body,
                # "raw_html" : raw_html,
                "crawl_date" : crawl_date,
                "sitename" : sitename,
                "url" : url
            }

            list_data.append(result)
            # print(list_data)
            break
        break




