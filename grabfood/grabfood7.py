import json
import sys
import requests
from selenium import  webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
import hashlib
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import beanstalkc

display = Display(visible=0, size=(1366, 768))
display.start()
cookies = {
    'gfc_country': 'MY',
    '_gsvid': '929ddb90-ed6d-4965-8ddc-938173a3b612',
    '_gcl_au': '1.1.85203650.1659577734',
    '_fbp': 'fb.1.1659577734380.2000435290',
    'hwuuidtime': '1659577767',
    'hwuuid': '1d17d3e1-39bb-4ade-904e-14a050fad8ae',
    '_hjSessionUser_1532049': 'eyJpZCI6IjI0MDU0ZjQyLWNjYjQtNWJlOS05ZTQwLThhNjIwZmIyOTI5NCIsImNyZWF0ZWQiOjE2NTk1Nzc3MzQzMjIsImV4aXN0aW5nIjp0cnVlfQ==',
    '_hjSessionUser_1740618': 'eyJpZCI6IjBlNmUxMDk2LTY2YjctNWNiMy1hOTJlLTYzMDFjOTEwMjI0MiIsImNyZWF0ZWQiOjE2NTk1Nzg1ODg2NjksImV4aXN0aW5nIjp0cnVlfQ==',
    '_gid': 'GA1.2.598720230.1660876866',
    'gfc_session_guid': 'a360c27b-02ac-41a9-a097-c74e2ce42a34',
    'next-i18next': 'en',
    '_gssid': '2207190356-tka0krd6duj',
    '_gcl_aw': 'GCL.1660881371.Cj0KCQjwuaiXBhCCARIsAKZLt3nBEiXsMGOphfU0aL5aNehiuV6bDgp83vais-8Fnls2YhyQ9-Xx5jEaAs5fEALw_wcB',
    '_gcl_dc': 'GCL.1660881371.Cj0KCQjwuaiXBhCCARIsAKZLt3nBEiXsMGOphfU0aL5aNehiuV6bDgp83vais-8Fnls2YhyQ9-Xx5jEaAs5fEALw_wcB',
    '_hjIncludedInSessionSample': '0',
    '_hjSession_1532049': 'eyJpZCI6IjMwNjhhOTY3LTViZDktNDA1YS1hNWM4LWI1MDc2ZTEzZDU1ZSIsImNyZWF0ZWQiOjE2NjA4ODEzNzA5ODQsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '_gac_UA-73060858-24': '1.1660881380.Cj0KCQjwuaiXBhCCARIsAKZLt3nBEiXsMGOphfU0aL5aNehiuV6bDgp83vais-8Fnls2YhyQ9-Xx5jEaAs5fEALw_wcB',
    'location': '%7B%22id%22%3A%22IT.3NR5R88F2JW96%22%2C%22latitude%22%3A1.640906%2C%22longitude%22%3A103.621549%2C%22address%22%3A%22Klinik%20Kesihatan%20Kulai%20Besar%20-%20Lebuhraya%20Senai%2C%20Bandar%20Putra%2C%20Kulai%2C%2081000%2C%20Johor%22%2C%22countryCode%22%3A%22MY%22%2C%22isAccurate%22%3Atrue%2C%22addressDetail%22%3A%22%22%2C%22noteToDriver%22%3A%22%22%2C%22city%22%3A%22Johor%20Bahru%20City%22%2C%22cityID%22%3A2%7D',
    '_ga_RPEHNJMMEM': 'GS1.1.1660881371.9.1.1660881414.17.0.0',
    '_ga': 'GA1.1.890299454.1659577734',
}

headers = {
    'authority': 'food.grab.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'gfc_country=MY; gfc_session_guid=f0b54018-e15a-4a78-9da4-e5b2a891ebe5; location=%7B%22latitude%22%3A3.139%2C%22longitude%22%3A101.6869%2C%22address%22%3A%22Kuala%20Lumpur%22%2C%22countryCode%22%3A%22MY%22%2C%22isAccurate%22%3Afalse%2C%22addressDetail%22%3A%22%22%2C%22noteToDriver%22%3A%22%22%2C%22city%22%3A%22%22%2C%22cityID%22%3A0%7D; next-i18next=en; _gssid=2207220459-27015nm0j3m; _gsvid=b68791cf-885c-4bdf-a591-c1f094a1561f; _gcl_au=1.1.877645113.1661144369; _hjSessionUser_1532049=eyJpZCI6Ijg4MTQ2MGNmLWI3OTEtNTk1ZC05ODlmLTIxYWZkNTRlODhkNiIsImNyZWF0ZWQiOjE2NjExNDQzNzAzODIsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample=0; _hjSession_1532049=eyJpZCI6ImU3MTVhM2U2LTYwODktNDU3Zi1hMjZmLTUwYzM2NWM5NjI4MiIsImNyZWF0ZWQiOjE2NjExNDQzNzA2OTMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _gid=GA1.2.569174201.1661144371; _gat_UA-73060858-24=1; _ga=GA1.1.926260073.1661144371; _ga_RPEHNJMMEM=GS1.1.1661144371.1.0.1661144370.60.0.0; hwuuid=90e854b2-ddeb-43eb-9b30-61995081db1d; hwuuidtime=1661144371; _fbp=fb.1.1661144371352.1026840181',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
}
# locations =
options = Options()
# options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
# browser = webdriver.Chrome(executable_path=r"E:\chromedriver.exe")
browser = webdriver.Chrome(executable_path="/home/shahid/crawler/grabfood/chromedriver", chrome_options=options)
df = pd.read_csv("/home/shahid/crawler/grabfood/clinic_joined_district.csv", sep='|', low_memory=False)
loop_clinic=0
for index, df2 in df.iterrows():
    loop_clinic = loop_clinic + 1
    if loop_clinic<=6097:
        continue
    if loop_clinic>7000:
        sys.exit()
    location = df2["name address"]
    state = df2["State"]
    district = df2["District"]
    clicic_name = df2["name"]
    address = df2["address"]
    print(clicic_name)


    browser.get("https://food.grab.com/my/en/restaurants?search=selangor")
    # wkwkwk
    time.sleep(5)
    browser.maximize_window()

    # browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div").click()
    WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div"))).click()
    try :
          # browser.find_element_by_id("location-input").send_keys(Keys.CONTROL, 'a')
          WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.ID, "location-input"))).send_keys(Keys.CONTROL, 'a')
          # browser.find_element_by_id("location-input").send_keys(Keys.BACKSPACE)
          WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.ID, "location-input"))).send_keys(Keys.BACKSPACE)
    except:
        pass
    # browser.find_element_by_id("location-input").send_keys(location)
    WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.ID, "location-input"))).send_keys(location)

    time.sleep(5)
    # browser.find_element_by_class_name("ant-select-dropdown-menu-item").click()
    WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-select-dropdown-menu-item"))).click()

    url = browser.current_url

    print("success location")
    b=True

    while b:
            # location_search = "?search=" + location.replace(" ", "%20")
            while True:
                # browser.get(url +location_search)
                # time.sleep(2)
                html = browser.page_source
                soup = BeautifulSoup(html,'html.parser')
                if "Oops, Something Went Wrong" in soup.get_text():
                    continue
                else:
                    break


            while True:
                try :

                    time.sleep(5)
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # browser.find_element_by_class_name("ant-btn").click()
                    element = browser.find_element_by_class_name('ant-btn')
                    browser.execute_script("arguments[0].click();", element)
                    print("success")
                    html = browser.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    if "Oops" in soup.get_text():
                        break

                    else:
                        continue
                except:
                    b=False
                    break

    try:
        html = browser.page_source
    except:
        continue
    soup = BeautifulSoup(html,'html.parser')
    # divs = soup.find("script", id="__NEXT_DATA__").get_text()
    # print(divs)
    divs = soup.find_all("div", class_="RestaurantListCol___1FZ8V")
    # divs = soup.find_all("div", class_="ant-col-24 RestaurantListCol___1FZ8V  ant-col-md-12 ant-col-lg-6")

    # time.sleep(5)\
    selected_location = soup.find("span", class_="textAddress___Rba2a").get_text()
    for div in divs:
        title = div.find("h6", class_="name___2epcT").get_text()
        type = div.find("div", class_="basicInfoRow___UZM8d cuisine___T2tCh").get_text()
        star = div.find("div", class_="numbersChild___2qKMV").get_text()

        if len(star) >3:
            star=""
            try:
                exclude_data = div.find("div", class_="numbersChild___2qKMV").get_text().split("•")
                estimate_time = exclude_data[0].strip()
                distcance = exclude_data[1].strip()
            except:
                estimate_time = ""
                distcance = ""
        else:
            try:
                exclude_data = div.find("div", class_="numbersChild___2qKMV").find_next("div", class_="numbersChild___2qKMV").get_text().split("•")
                estimate_time = exclude_data[0].strip()
                distcance = exclude_data[1].strip()
            except:
                estimate_time = ""
                distcance = ""



        url = div.find("a").attrs.get("href")
        url = "https://food.grab.com" + url
        print(url)

        try :
            discount = div.find("span", class_="discountText___GQCkj").get_text()
        except:
            discount=""

        # for div in data["hasMenu"]["hasMenuSection"]:


        result ={
            "title" : title,
            "type" : type,
            "star" : star,
            "discount" : discount,
            "estimate_time" : estimate_time,
            "distcance" : distcance,
            "location" : location,
            "selected_location" : selected_location,
            "state" : state,
            "district" : district,
            "clicic_name" : clicic_name,
            "address" : address,
            "url" : url,
        }

        print("loop_clinic : " + str(loop_clinic))
        print("clicic_name :" + clicic_name)




        beans = beanstalkc.Connection(host='42.1.61.117')
        beans.use("grabfood_link" )
        beans.put(json.dumps(result), 1, 0, 360000)
        # time.sleep(0.001)

    # with open(r"E:\result_grabfood_" + location + ".html", 'w', encoding='utf8') as outfile:
    #     outfile.write(str(soup))
    # with open(r"E:\result_grabfood_" + location + ".json", 'w',encoding='utf_8_sig') as outfile:
    #     json.dump(data21,outfile, ensure_ascii=False)
    name_file = hashlib.md5(clicic_name.encode('utf-8')).hexdigest().upper()
    with open("/dataph/one_time_crawling/home/grabfood/html/" + name_file + ".html", 'w', encoding='utf8') as outfile:
        outfile.write(str(soup))


    # with open("/dataph/one_time_crawling/home/grabfood/json/"  + name_file + ".json", 'w',encoding='utf_8_sig') as outfile:
    #     json.dump(data21,outfile, ensure_ascii=False)
# "wrapper___TJwRd borderless___1bvE8 addressBarInput"