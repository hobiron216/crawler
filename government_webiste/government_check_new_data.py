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
import os
from bs4 import BeautifulSoup
import codecs




df = pd.read_csv('/home/shahid/crawler/spider/government linked website database_v2.csv', sep='|', encoding='cp1252')
today = date.today()
crawl_date = today.strftime("%Y%m%d")

data=[]


for index, df2 in df.iterrows():
    sitename = df2['Website']
    base_url = df2['link']
    # print(sitename)
    a = 0
    z=""


    for root, dirs, files in os.walk("/dataph/government2/" + sitename + "/"):
       z="kwkwk"
       break

    if not z:
        data.append(sitename)
print(data)