import time
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
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


cookies = {
        'wcc-swipe-language': 'en-us',
    }

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJsdUN0YW5PQ0hNLUIxTi0xOUtEa0VxSFBqVF9MZ214TjBHdXZ3WjRmRURNIn0.eyJleHAiOjE2NDAwOTM1NjUsImlhdCI6MTY0MDA5MTc2NSwiYXV0aF90aW1lIjoxNjQwMDkxNzU3LCJqdGkiOiIzMGNmZTVkNC00ZjAyLTQzNTctOTRjYi05YTdjZjJkOTdkODQiLCJpc3MiOiJodHRwczovL2VtcGxveWVycy5teWZ1dHVyZWpvYnMuZ292Lm15L2F1dGgvcmVhbG1zL2VtcGxveWVycyIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzZmZiOTYwZC0yZDVhLTRlYWYtODYzMy0xZmJiZjZhNWEwNjciLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJlbXBsb3llcnMtYXBwIiwibm9uY2UiOiI2M2Q0ZDI4YS1lZDIyLTRlZTMtYjg2NS0xYjNkOGVmZTA3YmQiLCJzZXNzaW9uX3N0YXRlIjoiMDY3M2ZkOGUtMjJkNy00ZjM5LWFmNDctMmJlMGJjOGZkZDQ1IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2VtcGxveWVycy5teWZ1dHVyZWpvYnMuZ292Lm15Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiZW1wbG95ZXJzLWFwcCI6eyJyb2xlcyI6WyJFTSIsImVtcGxveWVyLXJvbGUiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtcGxveWVyX3BvcnRhbDphcHBsaWNhdGlvbl9tYW5hZ2VtZW50OmpvYnNlZWtlciB1c2VyX3Byb2ZpbGU6cmVhZCBqb2I6cmVhZCBlbXBsb3llcl9wb3J0YWw6dXBkYXRlOmNvbnRhY3QgZW1wbG95ZXJfcG9ydGFsOnVwZGF0ZTplbXBsb3llciBqb2JfYXBwbGljYXRpb246cmVhZCBlbXBsb3llcl9wb3J0YWw6aXNfYXNzaWduZWU6dmFjYW5jeSBwcm9maWxlIG9yZ2FuaXphdGlvbjpyZWFkIGpvYjp3cml0ZSBvcmdhbml6YXRpb246d3JpdGUgdXNlcl9wcm9maWxlOmltcG9ydCBlbXBsb3llcl9wb3J0YWw6dmlldzplbXBsb3llciBqb2I6ZGVsZXRlIG9yZ2FuaXphdGlvbjppbXBvcnQgam9iOmltcG9ydCBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXNlcl9pZCI6IjNmZmI5NjBkLTJkNWEtNGVhZi04NjMzLTFmYmJmNmE1YTA2NyIsIm5hbWUiOiJTSVRJIE5BSklIQUggQklOVEkgTU9IRCBZVVNPRiIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluLWViZGVzayIsImdpdmVuX25hbWUiOiJTSVRJIE5BSklIQUggQklOVEkgTU9IRCBZVVNPRiIsImZhbWlseV9uYW1lIjoiIiwiZW1haWwiOiJhZG1pbi1teUBlYmRlc2suY29tIn0.Dse0d-hikQSwr7sRUEJCpHgAKgTvptYPIifFnu6zQuwNLkn-Eb-uF9jPT2hbMXgcbvg0VlNfY7mqMRptmcxlv9BNiW-fVoJQ7kTqSsW4xHcZg17Ot5QRyzYkNFIWS47iCQH6bOkJS1LLOIwFSV-_xtY2BKOzLd7FtdkcJTFbCiose_2-FlJXdfYXnNY4Q8uMhFOQfZpReJdzhP88od4u3AYlH5ZRUrpbNctY9zUHfqSx0T6jm3_2rgzFnCmuCbkVBWBHuSDdCXYFsvzv_5mg8kNiiu46RhCeZd-0HQ0Kmcmovq8IE2Ng_kAdIazYHFFOUrlm3r1yPPesrLLtalqt2w',
   'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://employers.myfuturejobs.gov.my/vacancy/applicants?jobId=237b71348aaa4c068a33f758d6020d87',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
}
list_link =["/vacancy/applicants?jobId=237b71348aaa4c068a33f758d6020d87",
"/vacancy/applicants?jobId=8ed8ac4de1b346caac6721c0b79bde85",
"/vacancy/applicants?jobId=fd50a9ff12834aae95bc7458651a6c78",
"/vacancy/applicants?jobId=116f4bd004594ebab0c19961b194ba44",
"/vacancy/applicants?jobId=8bb8e1e37f614976a977596b136845d7",
"/vacancy/applicants?jobId=afc6622a61b1466aa57883731c810921",
"/vacancy/applicants?jobId=3f91465fd122400cbec98ca142f77c83",
"/vacancy/applicants?jobId=0a38d5ca72834efdbafd15170efa0a8a"]

#
# "/vacancy/applicants?jobId=fd50a9ff12834aae95bc7458651a6c78",
# "/vacancy/applicants?jobId=b49a01ead6f64c6fa17a710908b971db",
# "/vacancy/applicants?jobId=687e6860ce294919ab3ce92df7c483ac"]
z=-1

list_category = ["Jr Programmer", "BUSINESS ANALYST", "MANDARIN JOURNALIST", "SENIOR RESEARCH ASSISTANT", "JOURNALIST", "Internship Mandarin Journalist", "APACHE SPARK DEVELOPER", "INTERNSHIP JOURNALIST"]
for link in list_link:
    data21 = 0
    z=z+1
    category = list_category[z]
    category = category.replace(" ", "_")


    Path("/home/myfuturejob/" + crawl_date + "/" + category + "/").mkdir(parents=True, exist_ok=True)
    # Path("/home/myfuturejob/" + crawl_date + "/" + category + "/").mkdir(parents=True, exist_ok=True)
    id = link.split("=")[1]


    params = (
        ('limit', '10'),
        ('offset', '0'),
    )

    response = requests.get('https://employers.myfuturejobs.gov.my/api/vacancies/' + id + '/matchingJobseekers', headers=headers, params=params, cookies=cookies)
    # print(response.text)

    datas = json.loads(response.text)

    total_count = datas['totalCount']
    # total_count = int(total_count) + 1


    params = (
        ('limit', str(total_count)),
        ('offset', '0'),
    )
    while True:
        try:
            response = requests.get('https://employers.myfuturejobs.gov.my/api/vacancies/' + id + '/matchingJobseekers',
                                    headers=headers, params=params, cookies=cookies, timeout=10)
            break
        except requests.exceptions.RequestException as e:
            print("connetion timeout")
            continue

    # print(response.text)

    datas = json.loads(response.text)

    for data in datas['data']:
        id= data['id']
        # name = data['name']
        # name = str(name).strip().replace(" ", "_")
        # name = name.replace("/", "")
        # name = hashlib.md5(name.encode('utf-8')).hexdigest().upper()

        # if category == "Jr Programmer":
        #     if data21 <= 107:
        #         data21 = data21 + 1
        #         continue
        try :
            education_level_number = data['educationLevels'][0]
        except:
            education_level_number = ""
            education_level_desc = ""

        if education_level_number == "1":
            education_level_desc = "Primary Education or Below"
        elif education_level_number == "2":
            education_level_desc = "PMR / PT3 or Equivalent"
        elif education_level_number == "3":
            education_level_desc = "SPM / O Level / SKM Level 1 / SKM Level 2 / SKM Level 3 or Equivalent"
        elif education_level_number == "4":
            education_level_desc = "STPM / A Level or Equivalent"
        elif education_level_number == "5":
            education_level_desc = "Diploma / Advanced Diploma / Higher Graduate Diploma / DVM / DKM Level 4 / DLKM Level 5"
        elif education_level_number == "6":
            education_level_desc = "Bachelor's or Equivalent"
        elif education_level_number == "7":
            education_level_desc = "Master's or Equivalent "
        elif education_level_number == "8":
            education_level_desc = "Doctoral (PhD) or Equivalent t"

        data["education_level_desc"] = education_level_desc
        headers2 = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJsdUN0YW5PQ0hNLUIxTi0xOUtEa0VxSFBqVF9MZ214TjBHdXZ3WjRmRURNIn0.eyJleHAiOjE2NDAwOTM1NjUsImlhdCI6MTY0MDA5MTc2NSwiYXV0aF90aW1lIjoxNjQwMDkxNzU3LCJqdGkiOiIzMGNmZTVkNC00ZjAyLTQzNTctOTRjYi05YTdjZjJkOTdkODQiLCJpc3MiOiJodHRwczovL2VtcGxveWVycy5teWZ1dHVyZWpvYnMuZ292Lm15L2F1dGgvcmVhbG1zL2VtcGxveWVycyIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzZmZiOTYwZC0yZDVhLTRlYWYtODYzMy0xZmJiZjZhNWEwNjciLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJlbXBsb3llcnMtYXBwIiwibm9uY2UiOiI2M2Q0ZDI4YS1lZDIyLTRlZTMtYjg2NS0xYjNkOGVmZTA3YmQiLCJzZXNzaW9uX3N0YXRlIjoiMDY3M2ZkOGUtMjJkNy00ZjM5LWFmNDctMmJlMGJjOGZkZDQ1IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2VtcGxveWVycy5teWZ1dHVyZWpvYnMuZ292Lm15Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiZW1wbG95ZXJzLWFwcCI6eyJyb2xlcyI6WyJFTSIsImVtcGxveWVyLXJvbGUiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtcGxveWVyX3BvcnRhbDphcHBsaWNhdGlvbl9tYW5hZ2VtZW50OmpvYnNlZWtlciB1c2VyX3Byb2ZpbGU6cmVhZCBqb2I6cmVhZCBlbXBsb3llcl9wb3J0YWw6dXBkYXRlOmNvbnRhY3QgZW1wbG95ZXJfcG9ydGFsOnVwZGF0ZTplbXBsb3llciBqb2JfYXBwbGljYXRpb246cmVhZCBlbXBsb3llcl9wb3J0YWw6aXNfYXNzaWduZWU6dmFjYW5jeSBwcm9maWxlIG9yZ2FuaXphdGlvbjpyZWFkIGpvYjp3cml0ZSBvcmdhbml6YXRpb246d3JpdGUgdXNlcl9wcm9maWxlOmltcG9ydCBlbXBsb3llcl9wb3J0YWw6dmlldzplbXBsb3llciBqb2I6ZGVsZXRlIG9yZ2FuaXphdGlvbjppbXBvcnQgam9iOmltcG9ydCBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXNlcl9pZCI6IjNmZmI5NjBkLTJkNWEtNGVhZi04NjMzLTFmYmJmNmE1YTA2NyIsIm5hbWUiOiJTSVRJIE5BSklIQUggQklOVEkgTU9IRCBZVVNPRiIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluLWViZGVzayIsImdpdmVuX25hbWUiOiJTSVRJIE5BSklIQUggQklOVEkgTU9IRCBZVVNPRiIsImZhbWlseV9uYW1lIjoiIiwiZW1haWwiOiJhZG1pbi1teUBlYmRlc2suY29tIn0.Dse0d-hikQSwr7sRUEJCpHgAKgTvptYPIifFnu6zQuwNLkn-Eb-uF9jPT2hbMXgcbvg0VlNfY7mqMRptmcxlv9BNiW-fVoJQ7kTqSsW4xHcZg17Ot5QRyzYkNFIWS47iCQH6bOkJS1LLOIwFSV-_xtY2BKOzLd7FtdkcJTFbCiose_2-FlJXdfYXnNY4Q8uMhFOQfZpReJdzhP88od4u3AYlH5ZRUrpbNctY9zUHfqSx0T6jm3_2rgzFnCmuCbkVBWBHuSDdCXYFsvzv_5mg8kNiiu46RhCeZd-0HQ0Kmcmovq8IE2Ng_kAdIazYHFFOUrlm3r1yPPesrLLtalqt2w',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://employers.myfuturejobs.gov.my/vacancy/applicants?jobId=237b71348aaa4c068a33f758d6020d87',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        }

        # response = requests.get('https://employers.myfuturejobs.gov.my/api/profiles/resumes/' + str(id) + '/language/en-us', headers=headers, cookies=cookies, allow_redirects=True)
        # while True:
        #     try:
        #         response = requests.get(
        #             'https://employers.myfuturejobs.gov.my/api/profiles/resumes/' + str(id) + '/language/en-us',
        #             headers=headers2, cookies=cookies, timeout=10)
        #
        #         break
        #     except requests.exceptions.RequestException as e:
        #         print("connetion timeout")
        #         continue
        # try :
        #     open('/home/myfuturejob/' + crawl_date + '/' + category + '/' + name +'_cv.pdf',  'wb').write(response.content)
        # except:
        #     print("no pdf")
        #     continue

        with open('/home/myfuturejob/' + crawl_date + '/' + category + '/' + id +'.json', 'w', encoding='utf_8_sig') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

        data21 = data21 + 1
        print("total_data : " + str(data21))
        print("category : "  + category)
        print("total_count : " +  str(total_count))

        # open(r'E:\job3.pdf', 'wb').write(response.content)
        # with open(r'E:\tes_futerejob.json', 'w', encoding='utf_8_sig') as outfile:
        #     json.dump(data,outfile)



