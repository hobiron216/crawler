import requests
from bs4 import  BeautifulSoup

import requests
from dateutil import parser
import json
import  csv
import time
from datetime import date
from pathlib import Path
from csv import writer
from datetime import datetime
import datetime as datetime21
import re
import hashlib
import random
user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]

Path("/home/shahid/cims/").mkdir(parents=True,exist_ok=True)
random_sleep= [1,2,3,4,5,6]

cookies = {
    'ASP.NET_SessionId': '3momiaezvut4eu0prmjznurb',
    'ADRUM': 's=1626919088041&r=https%3A%2F%2Fcims.cidb.gov.my%2Fsmis%2Fregcontractor%2Freglocalsearchcontractor.vbhtml%3F0',
}


def get_paparan(paparan):
    data=[]
    registration_grade_and_category=[]
    result_ppk = ""
    result_sppk = ""
    result_stb = ""
    result_cca = ""


    cookies = {
        'ASP.NET_SessionId': '3momiaezvut4eu0prmjznurb',
        'ADRUM_BTa': 'R:0|g:d01f32b4-48ae-4ff4-8830-b6ed9827fb9c|n:customer1_39fb0ec9-aeb7-4ce6-80c0-d184fdc1ced8',
        'ADRUM_BT1': 'R:0|i:250|e:395',
        'ADRUM': 's=1626922218380&r=https%3A%2F%2Fcims.cidb.gov.my%2Fsmis%2Fregcontractor%2Freglocalsearch_view.vbhtml%3F-862098155',
    }

    user_agent = random.choice(user_agents)
    time.sleep(random.choice(random_sleep))
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    }

    # paparan = "7b0bc89d-1754-46a2-9226-07820cb64e0c"
    params = (
        ('search', 'P'),
        ('comSSMNo', paparan),
    )

    while True:
        try:
            response = requests.get('https://cims.cidb.gov.my/smis/regcontractor/reglocalsearch_view.vbhtml', headers=headers, params=params, cookies=cookies, timeout=5)
            break
        except:
            print("timeout")
            continue

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find("table").findAll("tr")

    a=0
    for div in divs:
        a=a+1

        if a==1:
            name = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()
        elif a==2:
            registered_address = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()
            registered_address = re.sub(' +', ' ', registered_address)
        elif a == 3:
            tel_no = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()
        elif a == 4:
            fax_no = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()
        elif a == 5:
            correspondence_address = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()
            correspondence_address = re.sub(' +', ' ', correspondence_address)
        elif a == 6:
            ppk_registration_no = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()
        elif a == 7:
            member_since = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()
        elif a == 8:
            current_registration_expiry_date = div.find("th").find_next("th").get_text().strip().replace("\r","").replace("\n","").strip()

            result_business_details = {
                "name" : name,
                "registered_address" : registered_address,
                "tel_no" : tel_no,
                "fax_no" : fax_no,
                "correspondence_address" : correspondence_address,
                "ppk_registration_no" : ppk_registration_no,
                "member_since" : member_since,
                "current_registration_expiry_date" : current_registration_expiry_date

            }




    divs2 = soup.find("table").find_next("table").findAll("tr")

    aw=0
    for div2 in divs2:
        aw=aw+1
        if aw==1:
            continue
        divs22 = div2.findAll("td")
        a = 0
        for div22 in divs22:
            a=a+1
            if a==1:
                grade = div22.get_text().strip().replace("\r","").replace("\n","").strip()
            elif a==2:
                category = div22.get_text().strip().replace("\r","").replace("\n","").strip()
                category = re.sub(' +', ' ', category)
            elif a == 3:
                specialization = div22.get_text().strip().replace("\r","").replace("\n","").strip()
                specialization = re.sub(' +', ' ', specialization)
                result_registration_grade_and_category = {
                    "grade" : grade,
                    "category" : category,
                    "specialization" : specialization
                }
                registration_grade_and_category.append(result_registration_grade_and_category)
    divs3 = soup.find("table").find_next("table").find_next("table").findAll("tr")
    z=0
    y1=0
    y2=0
    y3=0
    y4=0
    y_ppk=0
    y_sppk = 0
    y_stb = 0
    y_cca = 0
    ppk=[]
    sppk=[]
    stb=[]
    cca=[]

    for div3 in divs3:

       if "PPK" in div3.get_text():
            y_ppk = 1

       if "SPKK" in div3.get_text():
            y_sppk = 1

       if "STB" in div3.get_text():
           y_stb = 1

       if "CCA" in div3.get_text():
           y_cca = 1

       if y_ppk==1:
           y1=y1+1
           if y1>2:
                divs33 = div3.find_all("td", attrs={"style":"text-align:left;padding-left:10px"})
                # print(div3)
                # print("s======================================================================================")
                # print(divs33)
                a = 0
                for div33 in divs33:
                    a=a+1
                    if a==1:
                        jenis_tindakan_ppk = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==2:
                        tarikh_mula_ppk = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==3:
                        tarikh_akhir_ppk = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==4:
                        tarikh_batal_ppk = div33.get_text().strip().replace("\r","").replace("\n","").strip()

                        result_ppk = {
                            "jenis_tindakan_ppk" : jenis_tindakan_ppk,
                            "tarikh_mula_ppk" : tarikh_mula_ppk,
                            "tarikh_akhir_ppk" : tarikh_akhir_ppk,
                            "tarikh_batal_ppk" : tarikh_batal_ppk
                        }
                        ppk.append(result_ppk)

                        if "TINDAKAN" in div3.find_next("tr").find_next("tr").get_text():
                            y_ppk = 0
                        # y_ppk=0
                        print("ppk ada")
                        print(paparan)
                if not divs33:
                    y_ppk = 0
       if y_sppk==1:
           y2=y2+1
           if y2>2:

               divs33 = div3.find_all("td", attrs={"style": "text-align:left;padding-left:10px"})
               a = 0
               for div33 in divs33:
                   a = a + 1
                   if a == 1:
                       jenis_tindakan_sppk = div33.get_text().strip().replace("\r", "").replace("\n", "").strip()
                   elif a == 2:
                       tarikh_mula_sppk = div33.get_text().strip().replace("\r", "").replace("\n", "").strip()
                   elif a == 3:
                       tarikh_akhir_sppk = div33.get_text().strip().replace("\r", "").replace("\n", "").strip()
                   elif a == 4:
                        tarikh_batal_sppk = div33.get_text().strip().replace("\r", "").replace("\n", "").strip()

                        result_sppk = {
                            "jenis_tindakan_sppk" : jenis_tindakan_sppk,
                            "tarikh_mula_sppk" : tarikh_mula_sppk,
                            "tarikh_akhir_sppk" : tarikh_akhir_sppk,
                            "tarikh_batal_sppk" : tarikh_batal_sppk
                        }
                        sppk.append(result_sppk)
                        if "TINDAKAN" in div3.find_next("tr").find_next("tr").get_text():
                            y_sppk = 0
                        # y_sppk=0
                        print("sppk ada")
                        print(paparan)
               if not divs33:
                   y_sppk = 0
               # y_sppk = 0

       if y_stb == 1:
           y3 = y3 + 1
           if y3 > 2:
                # print(div3)
                divs33 = div3.findAll("td", attrs={"style":"text-align:left;padding-left:10px"})
                a = 0
                for div33 in divs33:
                    a=a+1
                    if a==1:
                        jenis_tindakan_stb = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==2:
                        tarikh_mula_stb = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==3:
                        tarikh_akhir_stb = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==4:
                       tarikh_batal_stb = div33.get_text().strip().replace("\r","").replace("\n","").strip()

                       result_stb = {
                           "jenis_tindakan_stb": jenis_tindakan_stb,
                           "tarikh_mula_stb": tarikh_mula_stb,
                           "tarikh_akhir_stb": tarikh_akhir_stb,
                           "tarikh_batal_stb": tarikh_batal_stb
                       }
                       stb.append(result_stb)
                       if "CCA" in div3.find_next("tr").find_next("tr").get_text():
                           y_stb = 0
                       # y_stb = 0
                       print("stb ada")
                       print(paparan)
                if not divs33:
                    y_stb = 0
                # y_stb = 0
       if y_cca == 1:
           y4 = y4 + 1
           if y4 > 2:

                divs33 = div3.findAll("td", attrs={"style":"text-align:left;padding-left:10px"})
                a = 0
                for div33 in divs33:
                    a=a+1
                    if a==1:
                        jenis_tindakan_cca = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==2:
                        tarikh_mula_cca = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==3:
                        tarikh_akhir_cca = div33.get_text().strip().replace("\r","").replace("\n","").strip()
                    elif a==4:
                       tarikh_batal_cca = div33.get_text().strip().replace("\r","").replace("\n","").strip()

                       result_cca = {
                           "jenis_tindakan_cca": jenis_tindakan_cca,
                           "tarikh_mula_cca": tarikh_mula_cca,
                           "tarikh_akhir_cca": tarikh_akhir_cca,
                           "tarikh_batal_cca": tarikh_batal_cca
                       }
                       cca.append(result_cca)
                       if "TINDAKAN" in div3.find_next("tr").get_text():
                           y_cca = 0
                       # y_cca = 0
                       print("cca ada")
                       print(paparan)
                if not divs33:
                    y_cca = 0
                # y_cca = 0
    result = {
        "business_details": result_business_details,
        "registration_grade_and_category" : registration_grade_and_category,
        "tindakan_tatatertib_ppk" :  ppk,
        "tindakan_tatatertib_spkk": sppk,
        "tindakan_tatatertib_stb": stb,
        "tindakan_cca": cca,
    }

    return result
    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://cims.cidb.gov.my/smis/regcontractor/reglocalsearch_view.vbhtml?search=P&comSSMNo=ff803927-d0a9-4b22-b5fd-0bfcc3689096', headers=headers, cookies=cookies)


i=-1
a=True
total_data=0
while a:
    if i==1:
        break
    i = i + 1
    print(i)
    user_agent = random.choice(user_agents)
    time.sleep(random.choice(random_sleep))
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://cims.cidb.gov.my',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://cims.cidb.gov.my/smis/regcontractor/reglocalsearchcontractor.vbhtml',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    }

    data = {
        'comName': '',
        'ComState': '',
        'ComCategoryID': '',
        'SSMNo': '',
        'ComDistrict': '',
        'ComSpecID': '',
        'ComGradeID': '',
        'seltype': '1',
        'selvalidity': '1',
        'hdnpagesize': '10',
        'hdnctpage': str(i),
        # 'hdntotpage': '124',
        'hdnsortcol': 'ComName',
        'hdnsortdir': '0',
        'hdntotalrecs': '123983',
        'hdnexportopts': '0',
        'txtgoto': '',
        'selpagesize': '10'
    }
    while True:
        try:
            response = requests.post('https://cims.cidb.gov.my/smis/regcontractor/reglocalsearchcontractor.vbhtml', headers=headers, cookies=cookies, data=data, timeout=5)
            break
        except:
            print("timeout")
            continue

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find("table").find_next("table").find_next("table").find_next("table").find_next("table").find_next("table").findAll("tr")
    # print(divs)

    aw=0
    if not divs:
        a=False
    for div in divs:
        aw=aw+1
        if aw==1:
            continue
        divs2 = div.findAll("td")
        # print(divs2)
        a = 0
        for div2 in divs2:
            a=a+1
            if a==1:
                continue
            elif a==2:
                nama_kontraktor=div2.get_text().strip()
            elif a==3:
                gred= div2.get_text().strip()
            elif a == 4:
                negeri = div2.get_text().strip()
            elif a == 5:
                daerah = div2.get_text().strip()
            elif a == 6:
                no_telefon = div2.get_text().strip()
            elif a == 7:
                no_faks = div2.get_text().strip()
            elif a == 8:
                ppk = div2.get_text().strip()
            elif a == 9:
                spkk = div2.get_text().strip()
            elif a == 10:
                stb = div2.get_text().strip()
            elif a == 11:
                paparan = div2.find("a").attrs.get("data-flag")
                result_paparan = get_paparan(paparan)


                result = {
                    "nama_kontraktor" : nama_kontraktor,
                    "gred" : gred,
                    "negeri" : negeri,
                    "daerah" : daerah,
                    "no_telefon" : no_telefon,
                    "no_faks" : no_faks,
                    "ppk" : ppk,
                    "spkk" : spkk,
                    "stb" : stb,
                    "paparan" : result_paparan,
                    "url_paparan" : "https://cims.cidb.gov.my/smis/regcontractor/reglocalsearch_view.vbhtml?search=P&comSSMNo=" + paparan
                }

                # nama_file = hashlib.md5(nama_kontraktor.encode('utf-8')).hexdigest().upper()
                total_data = total_data + 1
                with open("/home/shahid/cims/" + str(total_data) +'.json', 'w', encoding='utf8') as outfile:
                    json.dump(result, outfile)

                print("page : " + str(i))
                print("column : " + str(aw-1))
                print("total_data : " + str(total_data))
                # print(nama_file)
                print(nama_kontraktor)

                time.sleep(0.05)
    #     break
    # break





