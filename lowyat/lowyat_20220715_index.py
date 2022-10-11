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

Path("/news_cn/requests/lowyat/request_20220715/index/").mkdir(parents=True,exist_ok=True)

urls = ["https://forum.lowyat.net/StockExchange/", "https://forum.lowyat.net/Bitcoin&Cryptocurrencies/"]
loop_main_url=0
data=0



for url in urls:
    list_link = []
    result_json = []
    loop_main_url=loop_main_url+1

    if loop_main_url==1:
        name_file = "StockExchange"
    else:
        name_file = "Cryptocurrencies"

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
    summary=[]

    result_all = []
    today21= date.today()
    today = today21.strftime("%Y%m%d")
    yesterday =date.today() - datetime21.timedelta(1)


    name2=""
    comment2=""
    page=-30
    page_data=0

    while True:
        page_data = page_data+ 1
        page = page + 30
        link = url + "+" + str(page)
        while True:
            try:
                response = requests.get(link, headers=headers, timeout=5)
                break
            except:
                print("timeout")
                continue

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        if "Forum Topics" not in soup.get_text():
            break
        divs = soup.find("div", id="forum_topic_list").find("table").find_all("tr")


        loop_table=0
        for div in divs:
            loop_table = loop_table + 1
            #skip  pin forum
            if loop_main_url ==1:
                if page==0:
                    if loop_table<5:
                        continue
                else:
                    if loop_table<3:
                        continue
            else:
                if page == 0:
                    if loop_table < 4:
                        continue
                else:
                    if loop_table < 3:
                        continue

            # print(div)
            # sys.exit()
            try :
                topic_title = div.find("td", id="forum_topic_title").find("a").get_text()
                link_topic = div.find("td", id="forum_topic_title").find("a").attrs.get("href")
                link_topic = "https://forum.lowyat.net" + link_topic
                # list_link.append(link_topic)
                topic_desc = div.find("td", id="forum_topic_title").find("div", class_="desc").get_text()
                if topic_desc:
                    topic_title = topic_title + ", " + topic_desc
                topic_title = topic_title.replace("\n","").replace("\xa0","").strip()
                replies = div.find("td", id="forum_topic_replies").get_text().replace("\n","").replace("\xa0","").strip()
                topic_starter = div.find("td", id="forum_topic_ts").get_text().replace("\n","").replace("\xa0","").strip()
                views = div.find("td", id="forum_topic_views").get_text().replace("\n","").replace("\xa0","").strip()
            except:
                continue

            result = {
                "main_topic" : name_file,
                "topic_title": topic_title,
                "replies" : replies,
                "topic_starter": topic_starter,
                "views": views,
                "page" : page_data,
                "url" : link,
                "url_topic": link_topic,
                "crawl_date" : today
            }
            result_json.append(result)



            data=data+1
            print("jumlah data: " + str(data))
            print("page : " + str(page_data))
            print("main_topic : " + name_file)






        time.sleep(0.05)
        # break



    with open("/news_cn/requests/lowyat/request_20220715/index/" + name_file + ".json", 'w',
              encoding='utf_8_sig') as outfile:
        json.dump(result_json, outfile, ensure_ascii=False)


