import time
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from pathlib import Path

import os
import glob
import pandas as pd
# df = pd.read_csv(r'/home/crawler/otc/agoda/agoda_total_hotel.csv')
df = pd.read_csv(r'/home/crawler/otc/agoda/Travel_destinations_in_Malaysia_Total.csv')
total_hotel = 0
for region in df.values:
    region_name = region[0]



    total_hotel21 = region[4]
    try:
        total_hotel21 = int(total_hotel21)
    except:
        continue
    # print(total_hotel21)
    # break


    json_dir_name = '/dataph/one_time_crawling/home/agoda2/20211220/' + region_name

    json_pattern = os.path.join(json_dir_name, '*_*_detail.json')
    file_list = glob.glob(json_pattern)
    for file in file_list:
        total_hotel = total_hotel + 1
        # print(file)
        # with open(file, "r",  encoding='utf_8_sig') as outfile:
        #     datas = json.load(outfile)
        #     outfile.close()

    # if total_hotel != total_hotel21:
    #     print("salah!!!")
    #     print(region_name)
    # print("district :" + region_name)
print("total hotel : " + str(total_hotel))