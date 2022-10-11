import time
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from pathlib import Path

import os
import glob

cookies = {
        'wcc-swipe-language': 'en-us',
    }
# list_category = ["Jr Programmer"
list_category = ["Jr Programmer", "BUSINESS ANALYST", "MANDARIN JOURNALIST", "SENIOR RESEARCH ASSISTANT", "JOURNALIST",
                 "Internship Mandarin Journalist", "APACHE SPARK DEVELOPER", "INTERNSHIP JOURNALIST"]
a = 0
crawl_date = "20211221"
for category in list_category:
    data21 = 0
    category = category.replace(" ", "_")
    # print(category)
    # for root, dir, files in os.walk('/home/myfuturejob/20211221/' + category +'/*.json'):
    #     for file in files:
    #         print(file)

    json_dir_name = '/home/myfuturejob/20211221/' + category

    json_pattern = os.path.join(json_dir_name, '*.json')
    file_list = glob.glob(json_pattern)
    for file in file_list:
        with open(file, "r",  encoding='utf_8_sig') as outfile:
            datas = json.load(outfile)
            outfile.close()


        id = datas['id']
        try :
            with open("/home/myfuturejob/20211221/" + category + "/" + id + "_cv.pdf", "r",  encoding='utf_8_sig') as outfile2:
                outfile2.close()
        except:
            data_response =""
            # a=a+1
            # print("tidak ada")
            # print(category)
            # print(str(a))
            token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJsdUN0YW5PQ0hNLUIxTi0xOUtEa0VxSFBqVF9MZ214TjBHdXZ3WjRmRURNIn0.eyJleHAiOjE2NDAyMjk3MjgsImlhdCI6MTY0MDIyNzkyOCwiYXV0aF90aW1lIjoxNjQwMjI3OTE5LCJqdGkiOiJjYzM5ZjdhMC1mYjBjLTQ4ZWEtOGVkMC0yNmFhNDc1YTQ4ZGUiLCJpc3MiOiJodHRwczovL2VtcGxveWVycy5teWZ1dHVyZWpvYnMuZ292Lm15L2F1dGgvcmVhbG1zL2VtcGxveWVycyIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzZmZiOTYwZC0yZDVhLTRlYWYtODYzMy0xZmJiZjZhNWEwNjciLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJlbXBsb3llcnMtYXBwIiwibm9uY2UiOiIwYmNlNmRjMS0yMWM3LTRhZjItODdmMi0xZWFhNDM0MmMyNTUiLCJzZXNzaW9uX3N0YXRlIjoiMjcyMzU2MzQtN2U1MC00NTY1LWIzNmQtNTRlYzIzNmE0YmRhIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2VtcGxveWVycy5teWZ1dHVyZWpvYnMuZ292Lm15Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiZW1wbG95ZXJzLWFwcCI6eyJyb2xlcyI6WyJFTSIsImVtcGxveWVyLXJvbGUiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtcGxveWVyX3BvcnRhbDphcHBsaWNhdGlvbl9tYW5hZ2VtZW50OmpvYnNlZWtlciB1c2VyX3Byb2ZpbGU6cmVhZCBqb2I6cmVhZCBlbXBsb3llcl9wb3J0YWw6dXBkYXRlOmNvbnRhY3QgZW1wbG95ZXJfcG9ydGFsOnVwZGF0ZTplbXBsb3llciBqb2JfYXBwbGljYXRpb246cmVhZCBlbXBsb3llcl9wb3J0YWw6aXNfYXNzaWduZWU6dmFjYW5jeSBwcm9maWxlIG9yZ2FuaXphdGlvbjpyZWFkIGpvYjp3cml0ZSBvcmdhbml6YXRpb246d3JpdGUgdXNlcl9wcm9maWxlOmltcG9ydCBlbXBsb3llcl9wb3J0YWw6dmlldzplbXBsb3llciBqb2I6ZGVsZXRlIG9yZ2FuaXphdGlvbjppbXBvcnQgam9iOmltcG9ydCBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXNlcl9pZCI6IjNmZmI5NjBkLTJkNWEtNGVhZi04NjMzLTFmYmJmNmE1YTA2NyIsIm5hbWUiOiJTSVRJIE5BSklIQUggQklOVEkgTU9IRCBZVVNPRiIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluLWViZGVzayIsImdpdmVuX25hbWUiOiJTSVRJIE5BSklIQUggQklOVEkgTU9IRCBZVVNPRiIsImZhbWlseV9uYW1lIjoiIiwiZW1haWwiOiJhZG1pbi1teUBlYmRlc2suY29tIn0.TsAlE472CdpxX3NB2AH6gdy36ZaKx2gxFbB8C7y1MLSB_gH62ie6By0QfW1ACOb7lZh2p4_vL8w8LIMBnCiIk9cFmonUjqmGrcEG1pLbnfqyDh0iL3h81hoOlzERx1bsDmc6470FleqCUiLv4IKkKTOSfm3gkQIm6rviBxo26vn-uY8DYAfF962iKI2my1YM5cCnwa70qxarQ5Tcg5Tw4PNMkLFs03cd7kDNzA8KYr1OvZ9DkMTfzGN7a1mTw748iEL7zmQQJ7hCDhkFz7-rcM9a9L8uT97wqDDVfVUOuhpdqYUG7uGEPJ2EevBmrw-YXsLCmcZZnZJnkuEV7XADTA"
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
                    print("pdf tidak ada")
                    test = 0
                    print("total_data : " + str(data21))
                    print("category : " + category)
                    # 21
            data_response = response.content
            open('/home/myfuturejob/' + crawl_date + '/' + category + '/' + id + '_cv.pdf', 'wb').write(data_response)
            data21 = data21 + 1
            print("total_data : " + str(data21))
            print("category : " + category)