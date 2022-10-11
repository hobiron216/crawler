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
import hashlib

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

Path("/news_cn/requests/lowyat/batch2/").mkdir(parents=True,exist_ok=True)


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
list_link=[]
result_all = []
today21= date.today()
today = today21.strftime("%Y%m%d")
yesterday =date.today() - datetime21.timedelta(1)









# with open("last_page.txt", 'r', encoding='utf8') as outfile:
#     r=outfile.read()
#
# with open("last_page_kemarin.txt", 'w', encoding='utf8') as outfile:
#     outfile.write(str(r))
# i = int(r) - 20
# i = 720


page =-30
b= True
while b:
    page = page+30
    base_link="https://forum.lowyat.net/Bitcoin&Cryptocurrencies/+" + str(page)
    r= requests.get(base_link)
    soup2= BeautifulSoup(r.text,'html.parser')
    divs= soup2.find("table").find_next("table").findAll("tr")
    z=0
    if page>510:
        break
    for div in divs:


        try:
            links = div.find("a").attrs.get("href")
            list_link.append(links)
            # print(links)
        except:
            continue
    for link21 in list_link:
        name_file21 = "https://forum.lowyat.net/" + link21
        name_file = hashlib.md5(name_file21.encode('utf-8')).hexdigest().upper()
        fields = ['page_forum', 'page_url', 'topic', 'comment_name', 'comment_time', 'converted_time', 'comment']

        with open("/news_cn/requests/lowyat/batch2/" + name_file + '.csv', "w", encoding='utf-8', newline="") as f:
            write = csv.writer(f, quoting=csv.QUOTE_ALL)
            write.writerow(fields)

        z=z+1
        name2=""
        comment2=""
        i=-20
        a=True
        while a:
            i = i + 20
            link = "https://forum.lowyat.net/" + link21 + "/+" + str(i)

            while True:
                try:
                    response = requests.get(link, headers=headers, timeout=5)
                    break
                except:
                    print("timeout")
                    continue

            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            divs = soup.findAll("table", class_="post_table")
            topic = soup.find("title").get_text()


            a=0
            for div in divs:
                a = a + 1
                name = div.find("span", class_="normalname").get_text().strip()



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
                # result = {
                #     "name": name,
                #     "comment_time": str(comment_time),
                #     "converted_time": str(converted_time),
                #     "comment": str(comment)
                # }
                list =[base_link, link, topic,  name, comment_time, converted_time, comment]
                if len(link)>60:
                    continue
                # print(list)
                with open('/news_cn/requests/lowyat/batch2/' + name_file + '.csv', 'a',  newline='', encoding='utf-8') as f_object:

                    writer_object = writer(f_object)


                    writer_object.writerow(list)

                    # Close the file object
                    f_object.close()
            print("page_all :" +  str(page/30))
            print("forum ke- :" + str(z))
            print("page_form :" + str(i/20))

            time.sleep(0.05)
    del list_link[:]




# with open("last_page.txt", 'w', encoding='utf8') as outfile:
#     outfile.write(str(i-20))

# message = "Engine : lowyat \n Page : " + str((i-20)/20+1)
# telegram_bot_sendtext(str(message))
# print("terkirim")
