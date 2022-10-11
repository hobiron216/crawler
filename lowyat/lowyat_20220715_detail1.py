import sys

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

def telegram_bot_sendtext(bot_message):
    global response
    bot_token = '1381123927:AAEQ169ZfG5qQMvPaNaFyt8zBJzyeZ-feXc'
    bot_chatID = '1008898421'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    while True:
        try:
            response = requests.get(send_text, timeout=10)
            break
        except requests.exceptions.RequestException as e:
            print("gagal kirim telegram")
            continue

    return response.json()




headers = {
    'authority': 'forum.lowyat.net',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'cookie': 'lyn_mobile=0; lyn_modtids=%2C; __auc=bf0d4a1217a75aba33f54935843; _gid=GA1.2.1048712458.1625471822; lyn_forum_read=a%3A1%3A%7Bi%3A321%3Bi%3A1625471889%3B%7D; __asc=d178d28a17a75d922fe18aaa41c; _ga_ZC0B7MQG59=GS1.1.1625474616.2.1.1625476204.0; _ga=GA1.2.683055162.1625471821; _gat_gtag_UA_144730_46=1; _gat_gtag_UA_144730_48=1; __cf_bm=34ab2c094985c476f9dd23a1a65f4fbcaa448433-1625476205-1800-AY3WGlEsc/j/N6y/kTnHJXk0nd6gXDOcg7WlgUfj71Hp72S9e3E/hzd5l0mXz5EBfWaV9+taOMRprRxXdfteQnZzNYPQVWqxSbGgHEz0kLN8mdnOojRCBGf02wmvNGZdUQ==; __gads=ID=25098e03e5b5844a:T=1625476205:S=ALNI_MbUNQLWQ7X3Q6aFeMsAIcprzj4ANw',
}

today21= date.today()
today = today21.strftime("%Y%m%d")
yesterday =date.today() - datetime21.timedelta(1)


urls = ["https://forum.lowyat.net/StockExchange/", "https://forum.lowyat.net/Bitcoin&Cryptocurrencies/"]
loop_main_url=0
data=0
Path("/news_cn/requests/lowyat/request_20220715/detail/Cryptocurrencies/").mkdir(parents=True,exist_ok=True)
with open("/news_cn/requests/lowyat/request_20220715/index/Cryptocurrencies.json", 'r',  encoding='utf-8-sig') as outfile:
    data_jsons = outfile.readline()
    data_jsons = json.loads(data_jsons)




for data_json in data_jsons:

    result_json=[]
    main_topic = data_json["main_topic"]
    topic_title = data_json["topic_title"]
    url = data_json["url_topic"]
    nama_file = url.split("/")[4]

    name2=""
    comment2=""
    page=-20
    page_data = 0
    a=True
    while a:
        page_data = page_data + 1
        page = page + 20
        link = url + "/+" + str(page)
        print(link)
        while True:
            try:
                response = requests.get(link, headers=headers, timeout=5)
                break
            except:
                print("timeout")
                continue

        url_check = response.url
        if url_check !=link:
            break

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll("table", class_="post_table")



        a=0
        for div in divs:
            a = a + 1
            name = div.find("span", class_="normalname").get_text().strip()
            user_details = div.find("span", class_="postdetails").find_next("span", class_="postdetails").find_next("span", class_="postdetails")
            user_detail = user_details.get_text().replace("\n"," ").replace("\t"," ").strip()
            user_detail = re.sub(' +', ' ', user_detail)

            # stars = user_details.find("div", class_="avatar").find_all("img")
            # star=-1
            # for star21 in stars:
            #     star = star + 1
            # print(star)


            comment_time = div.find("span", class_="postdetails").get_text().strip()
            split_time = comment_time.split(",")

            if "Yesterday" in comment_time:
                converted_time = datetime.strptime(str(split_time[1]).strip(), '%I:%M %p')
                converted_time = str(converted_time).split(" ")[1]
                converted_time = str(yesterday) + " " + str(converted_time)
            elif "Today" in comment_time:
                converted_time = datetime.strptime(str(split_time[1]).strip(), '%I:%M %p')
                converted_time = str(converted_time).split(" ")[1]
                converted_time = str(today) + " " + str(converted_time)
            else:
                comment_time= split_time[0] + split_time[1]
                converted_time = datetime.strptime(comment_time, '%b %d %Y %I:%M %p')

            converted_time = str(converted_time).replace("-", "")

            divs2 = soup.findAll("div", class_="postcolor post_text")
            b=0
            for div2 in divs2:
                b=b+1

                if a!=b:
                    continue
                comment = div2.get_text().strip()
            # comment= div.find("div", class_="postcolor post_text").get_text()
            if name == name2 and comment==comment2:
                a = False
            if a == 1:
                name2 = name
                comment2 = comment
            result = {
                "main_topic" : main_topic,
                "topic_title" : topic_title,
                "user": name,
                "user_detail" : user_detail,
                "comment_time": str(comment_time),
                "converted_time": str(converted_time),
                "comment": str(comment),
                "url" : link,
                "crawl_date" : today
            }
            result_json.append(result)

            data = data + 1
            print("jumlah data: " + str(data))
            print("page : " + str(page_data))
            print("topic_id : " + nama_file)
            # print("topic_title : " + topic_title)


        time.sleep(0.05)


    with open("/news_cn/requests/lowyat/request_20220715/detail/" + main_topic + "/" + nama_file + ".json", 'w', encoding='utf_8_sig') as outfile:
        json.dump(result_json, outfile, ensure_ascii=False)
    # sys.exit()
# print(result)
# sys.exit()
# with open("last_page.txt", 'w', encoding='utf8') as outfile:
#     outfile.write(str(i-20))
#
# message = "Engine : lowyat \n Page : " + str((i-20)/20+1)
# telegram_bot_sendtext(str(message))
# print("terkirim")
