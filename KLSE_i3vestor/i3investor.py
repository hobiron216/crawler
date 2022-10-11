import requests
from bs4 import  BeautifulSoup

import requests
from dateutil import parser
import json


base_link="https://klse.i3investor.com/"

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
user_comments=[]

for i in range (1,102):
    url = "https://klse.i3investor.com/servlets/cube/post/mikecyc.jsp?fp=" + str(i)
    response = requests.get(url, headers=headers)
    html=response.text

    soup = BeautifulSoup(html,'html.parser')
    divs1 = soup.findAll("td", class_="prftabtext")
    if i==1:
        z=0
        for div1 in divs1:
            z=z+1

            if z==1:

                total_comments = div1.find_next().get_text()
            elif z==2:
                past_30_days = div1.find_next().get_text()

            elif z==3:
                past_7_days = div1.find_next().get_text()

            elif z==4:
                today= div1.find_next().get_text()
        result={
            "total_comments" : str(total_comments),
            "past_30_days" : str(past_30_days),
            "past_7_days" : str(past_7_days),
            "today" : str(today),
        }


    divs2 = soup.find_all("td", attrs={"style" : "word-wrap: break-word;text-align:left;"})
    y=0
    for div2 in divs2:
        title = div2.find("p", class_="forumtopic").get_text()
        title_url = base_link + div2.find("a").attrs.get("href")
        comment_time = div2.find("span", class_="comdt").get_text()

        converted_time =str(parser.parse(comment_time)).replace("-","")
        comment = div2.find("p", class_="autolink").get_text()
        if "Post removed." in comment:
            comment=comment.replace("Why?","")
        # comment=str(comment).strip().encode("utf-8")



        result_comment ={
            "title" : str(title),
            "title_url" : str(title_url),
            "comment_time" : str(comment_time),
            "converted_time" : str(converted_time),
            "comment" : str(comment)
        }
        user_comments.append(result_comment)
        # y=y+1
        # if y==30:
        #     break
    print(i)
result["user_comments"] = user_comments
# print(result)
with open("/i3investor2.json", 'w', encoding='utf8') as outfile:
    json.dump(result, outfile, ensure_ascii=False)
# aw=json.loads(str(result))
# print(aw)

