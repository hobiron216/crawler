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

Path("/news_cn/requests/KLSE_i3vestor/request/").mkdir(parents=True,exist_ok=True)
base_link="https://klse.i3investor.com/"
stock_url = "https://klse.i3investor.com/jsp/scl/forum.jsp?c=1"
news_url = "https://klse.i3investor.com/jsp/scl/forum.jsp?c=2"

headers = {
    'authority': 'klse.i3investor.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'cookie': '__atvuca_dfp1=1623723737972mye524e8eeabba4a4f3aa8d1daa7cb5c4a3223806; JSESSIONID=AD3DE80227D17DBA61D56F3EABD54485; __asc=c75827b317a0d7a0796b75e0e4e; __auc=c75827b317a0d7a0796b75e0e4e; _ga=GA1.2.1247685865.1623723739; _gid=GA1.2.1902098681.1623723739; ww=961; hh=737; _gat_gtag_UA_15537057_1=1',
}
summary=[]
list_link=[]
result_all = []
today = date.today()
crawl_date = today.strftime("%Y%m%d")

List=[1,2,3,4,5,6]






with open("last_page.txt", 'r', encoding='utf8') as outfile:
    r=outfile.read()

with open("last_page_kemarin.txt", 'w', encoding='utf8') as outfile:
    outfile.write(str(r))
i = int(r) - 1
# i = 720
def user_comments(divs2):
    user_comments=[]

    for div2 in divs2:

        name = div2.find("span", class_="comuid").get_text()
        comment_time = div2.find("span", class_="comdt").get_text()

        converted_time = str(parser.parse(comment_time)).replace("-", "")
        try:
            comment = div2.find("span", class_="autolink").get_text()

            # comment=str(comment).strip().encode("utf-8")
        except:
            comment = "Post removed."

        result_comment = {
            "name": name,
            "comment_time": str(comment_time),
            "converted_time": str(converted_time),
            "comment": str(comment)
        }
        user_comments.append(result_comment)

    return user_comments


while True:
    i=i+1
    print(i)
    link = "https://klse.i3investor.com/servlets/forum/800005607.jsp?ftp=" + str(i)
    response2 = requests.get(link, headers=headers)
    # print(link)
    html2 = response2.text
    soup2 = BeautifulSoup(html2, 'html.parser')
    divs2 = soup2.findAll("td", attrs={"style": "word-wrap: break-word;"})

    if "Posted by" not in html2:
        break

    titles = soup2.find("span", attrs={"style": "font-size:16px;"})
    title = titles.get_text()
    title_url = base_link + titles.find("a").attrs.get("href")
    result = {
        "title": str(title),
        "title_url": str(title_url),
        "url" : link
    }

    user_comments21= user_comments(divs2)


    result["user_comments"] = user_comments21

    # result_all.append(result)
    for user_comment21 in user_comments21:
        list =[title, title_url, link, user_comment21['name'], user_comment21['comment_time'], user_comment21['converted_time'], user_comment21['comment']]
        with open('/news_cn/requests/KLSE_i3vestor/request/KLSE_i3vestor_stock_requests.csv', 'a', encoding='utf-8') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            # print(str(list).encode("ascii","ignore").decode())

            writer_object.writerow(list)

           # Close the file object

            f_object.close()
    time.sleep(0.05)
    # break
#
# fields=['title','title_url','page_url','comment_name','comment_time','converted_time','comment']
# lr = []
# if result_all:
#     for j in result_all :
#         for c in j['user_comments'] :
#             tmp = []
#             tmp.append(j['title'])
#             tmp.append(j['title_url'])
#             tmp.append(j['url'])
#             tmp.append(c['name'])
#             tmp.append(c['comment_time'])
#             tmp.append(c['converted_time'])
#             tmp.append(c['comment'])
#             lr.append(tmp)




with open("last_page.txt", 'w', encoding='utf8') as outfile:
    outfile.write(str(i))

message = "Engine : klse \n Page : " + str(i)
telegram_bot_sendtext(str(message))
# print("terkirim")
