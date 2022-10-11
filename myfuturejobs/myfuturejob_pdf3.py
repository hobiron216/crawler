import sys
import time
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from pathlib import Path
import re
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import glob


#sample id ngga ada pdf : fe570d39-f10d-45bc-8a85-52cd739e8bc1 , c2ab78f8-52f2-41aa-9b44-361c291db8d7

# browser = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")
# browser.get("https://employers.myfuturejobs.gov.my/auth/realms/employers/protocol/openid-connect/auth?client_id=employers-app&redirect_uri=https%3A%2F%2Femployers.myfuturejobs.gov.my%2F%3Fui_locales%3Den-us%26kc_locale%3Den-us&state=8c886335-ac98-4f95-8cf9-15f37275954a&response_mode=fragment&response_type=code&scope=openid&nonce=3080f095-daf0-490c-8e81-c50553d95191&ui_locales=en-us")
# browser.find_element(By.ID,'username').send_keys("admin-ebdesk")
# browser.find_element(By.ID,'password').send_keys("Rahasia@0@0")
# browser.find_element(By.ID,'kc-login').click()
# time.sleep(10)
#
# html = browser.page_source
#
# soup = BeautifulSoup(html, 'html.parser')
# divs = soup.findAll("a", class_="list__item d-block")
# list_link = []
# for div in divs:
#     url = div.attrs.get("href")
#     check = div.find("span", class_="text-decoration-line-through")
#     if not check:
#         list_link.append(url)

today = date.today()
crawl_date = today.strftime("%Y%m%d")
crawl_date = "20211221"


cookies = {
        'wcc-swipe-language': 'en-us',
    }

test = 0

token_count = 0
with open('header.json', 'r') as outfile:
    token = json.load(outfile)
    token = token[token_count]
    outfile.close()
# list_category = ["BUSINESS ANALYST", "MANDARIN JOURNALIST", "SENIOR RESEARCH ASSISTANT", "JOURNALIST", "Internship Mandarin Journalist", "APACHE SPARK DEVELOPER", "INTERNSHIP JOURNALIST"]
list_category = ["APACHE SPARK DEVELOPER"]#, "INTERNSHIP JOURNALIST"]
a ="sgs"
for category in list_category:
    data21 = 0
    category = category.replace(" ", "_")
    # print(category)
    # for root, dir, files in os.walk('/home/myfuturejob/20211221/' + category +'/*.json'):
    #     for file in files:
    #         print(file)

    contents = []
    json_dir_name = '/home/myfuturejob/20211221/' + category

    json_pattern = os.path.join(json_dir_name, '*.json')
    file_list = glob.glob(json_pattern)
    aw =0
    for file in file_list:
        with open(file, "r",  encoding='utf_8_sig') as outfile:
            datas = json.load(outfile)
        aw = aw + 1
        if category == "APACHE_SPARK_DEVELOPER":
            if aw<4205:
                data21 = aw
                continue


        id = datas['id']

        # if a=="sgs":
        #     print("drhhdx")
        #     if id =="fdd092a3-1e5f-435d-8b93-725fe55d1657":
        #         a="wkwkwk"
        #         print(a)
        #     data21 = data21 + 1
        #     continue


        print(id)
        data_response=""
        while True:
            while True:
                try:
                    headers = {
                        'Connection': 'keep-alive',
                        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
                        'Accept': 'application/json, text/plain, */*',
                        'Authorization': token,
                        'sec-ch-ua-mobile': '?0',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
                        'sec-ch-ua-platform': '"Windows"',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Dest': 'empty',
                        'Referer': 'https://employers.myfuturejobs.gov.my/vacancy/applicants?jobId=e9cc369863c049b0815ace36deabf08e',
                        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
                    }
                    response = requests.get('https://employers.myfuturejobs.gov.my/api/profiles/resumes/' + id + '/language/en-us', headers=headers, cookies=cookies, timeout=30)
                    break
                except requests.exceptions.RequestException as e:
                    test= test + 1
                    if test==1:
                        print("connetion timeout")
                        print(id)
                        with open('header.json', 'r') as outfile:
                            token_count = token_count + 1
                            try:
                                token = json.load(outfile)
                                token = token[token_count]
                            except:
                                token_count = token_count - 1
                                print("need new token")
                            outfile.close()
                        continue
                    else:
                        print("pdf tidak ada")
                        test = 0
                        print("total_data : " + str(data21))
                        print("category : " + category)
                        break
            data_response = response.content
            if not data_response:
                test = test + 1
                if test == 1:
                    print("header expired")
                    with open('header.json', 'r') as outfile:
                        token_count = token_count + 1
                        token = json.load(outfile)
                        try :
                            token = token[token_count]
                        except:
                            token_count = token_count - 1
                            print("need new token")

                        outfile.close()

                    continue
                else:
                    print("pdf tidak ada")
                    test = 0
                    print("total_data : " + str(data21))
                    print("category : " + category)
                    break


            try :
                    open('/home/myfuturejob/' + crawl_date + '/' + category + '/' + id +'_cv.pdf',  'wb').write(data_response)
                    data21 = data21 + 1
                    print("total_data : " + str(data21))
                    print("category : " + category)
                    print("token_count : " + str(token_count))
                    break
            except Exception as e:
                print(e)
                print("no pdf")
                print("category : " + category)
                print("total_data : " + str(data21))
                sys.exit()
                break

print("total_data : " + str(data21))
print("category : " + category)







