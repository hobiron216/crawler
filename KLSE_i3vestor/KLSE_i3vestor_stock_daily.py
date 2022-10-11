import requests
from bs4 import  BeautifulSoup

import requests
from dateutil import parser
import json
from pathlib import Path
import time
import random
import hashlib
import csv
from csv import writer

Path("/news_cn/requests/KLSE_i3vestor/stock/daily2/").mkdir(parents=True,exist_ok=True)
base_link="https://klse.i3investor.com/"
stock_url = "https://klse.i3investor.com/jsp/scl/forum.jsp?c=1"
news_url = "https://klse.i3investor.com/jsp/scl/forum.jsp?c=2"


user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]


summary=[]

list_link=[]
result_all = []
i=0
proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
random_sleep= [1,2,3,4,5,6,7,8,9,10]

def user_comments(divs2,link):
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

        result = {
            "url" : link
        }
        result["user_comments"] = user_comments

    return result
while True:
    i=i+1
    # if i < 58:
    #     continue
    #     # if z<17:
    #     continue
    url = stock_url + "&fp=" + str(i)
    user_agent = random.choice(user_agents)
    headers = {
        'authority': 'klse.i3investor.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://klse.i3investor.com/jsp/scl/forum.jsp',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        '$cookie': '__atvuca_dfp1=1623723737972mye524e8eeabba4a4f3aa8d1daa7cb5c4a3223806; __auc=c75827b317a0d7a0796b75e0e4e; _gid=GA1.2.1902098681.1623723739; _pbjs_userid_consent_data=3524755945110770; _ga_0DTZ6LRDBJ=GS1.1.1623816829.1.1.1623816829.60; _cc_id=c1aecb0559d179523938930ddf75fe86; pubmatic-unifiedid=%7B%22TDID%22%3A%22b59601aa-b224-4a62-a118-7334aabce0d8%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-05-16T04%3A13%3A52%22%7D; id5_storage=%7B%22created_at%22%3A%222021-06-16T04%3A13%3A53.038836Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5-ZHMOAjEH8vsmgppmtG1WRiXdKW_4MJ9IeQgWFkgRlA\\u0021ID5*QPjbqxiBkRbhlhR-fAT7slyVS811SKZ7Usme8gz4h3AAAHgteUWsOjKD91PvbZTM%22%2C%22universal_uid%22%3A%22ID5-ZHMOYsn_fIeHjRdg03tp7541bpDsLL6ChB9mNRN7cg\\u0021ID5*2XLP8-HzfcAEvQ-r4-n51Wykt9IT1q4CAb6d2rYp-c4AAMVVOHrbqyRxgfDyQUYe%22%2C%22signature%22%3A%22ID5_Aee-6icAlfo1z2r7DkmWWHovWH98LNijQ8AlL5Wd99CEWR9Pfwkfl01cE5_SIwAPNKQm9F0kdt84NKoaJlbuyJo%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; _ga=GA1.2.1247685865.1623723739; __gads=ID=7c8f771ce9284ebc:T=1623816827:S=ALNI_MZq8bpHYDnT-u32y0PaxE3hWZQuMw; cto_bidid=p2Ie919udVdHWiUyQnNpaWduOGlyRFRnTzhCMXhFelpneDdFeVBLM2xUR1Yyd3JyTHNxTUtocFR0RkhKT3JYJTJCbUxjWUxOdXhReFFJQ3JZcHZod2FiWEglMkIxTm9YRFJMaSUyRmxjNTdVSDV2cjB5TVc2WE5RJTJGejdRekdQYTRMd2x1WjkxOEJjMW4; cto_bundle=vk6NfF9VUUpSSmhPSkZ6ZGN6Q2twZjU5eDZrQnowU3FnQ2xsTDVnc3hicmVJU2llRlJpUGp1eUVXN0NCMUJSSXZGUHFKaXBpVm5NVHFENm9JMm16VHEybnhoR1k0cjlvM3JiM1hJVG14V3dVam8xRGxpcXpERFZDMmc1cEdtV0lYbEFVS1JTM1E1RnVDOFFEQmVKT21YR2NNTEElM0QlM0Q; hh=969; ww=1344; JSESSIONID=02EC7E8E7D0F07E96AC14C9046CA3AF4; __asc=90123ff317a15bd38f818a6ef1f; _gat_gtag_UA_15537057_1=1; __atuvc=237%7C24; __atuvs=60ca2c58227e3aed003',
    }
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            break
        except:
            # print("looping forum")
            continue
    html=response.text
    soup = BeautifulSoup(html,'html.parser')
    # print(html)


    divs = soup.findAll("td", attrs={"style" : "padding-bottom:10px;word-wrap: break-word;"})
    z=0
    for div in divs:
        z=z+1
        if "No discussion entries available." in div:
            break
        link = base_link + div.find("a").attrs.get("href")

        j=0
        save_comment = ""
        while True:
            daily_page=""
            time.sleep(random.choice(random_sleep))
            j=j+1
            name_file = hashlib.md5(link.encode('utf-8')).hexdigest().upper()
            try:
                with open("/home/crawler/KLSE_i3vestor/page_daily/last_page_" + name_file +  ".txt", 'r', encoding='utf8') as outfile:
                    r_page = outfile.read()
                    daily_page = int(r_page)
            except:
                print("wkwkwk")
            if daily_page:
                url2 = link + "?ftp=" + str(daily_page)
            else:
                url2 = link + "?ftp=" + str(j)
            print("link : " + str(url2))



            user_agent2 = random.choice(user_agents)
            headers2 = {
                'authority': 'klse.i3investor.com',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://klse.i3investor.com/jsp/scl/forum.jsp',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                '$cookie': '__atvuca_dfp1=1623723737972mye524e8eeabba4a4f3aa8d1daa7cb5c4a3223806; __auc=c75827b317a0d7a0796b75e0e4e; _gid=GA1.2.1902098681.1623723739; _pbjs_userid_consent_data=3524755945110770; _ga_0DTZ6LRDBJ=GS1.1.1623816829.1.1.1623816829.60; _cc_id=c1aecb0559d179523938930ddf75fe86; pubmatic-unifiedid=%7B%22TDID%22%3A%22b59601aa-b224-4a62-a118-7334aabce0d8%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-05-16T04%3A13%3A52%22%7D; id5_storage=%7B%22created_at%22%3A%222021-06-16T04%3A13%3A53.038836Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5-ZHMOAjEH8vsmgppmtG1WRiXdKW_4MJ9IeQgWFkgRlA\\u0021ID5*QPjbqxiBkRbhlhR-fAT7slyVS811SKZ7Usme8gz4h3AAAHgteUWsOjKD91PvbZTM%22%2C%22universal_uid%22%3A%22ID5-ZHMOYsn_fIeHjRdg03tp7541bpDsLL6ChB9mNRN7cg\\u0021ID5*2XLP8-HzfcAEvQ-r4-n51Wykt9IT1q4CAb6d2rYp-c4AAMVVOHrbqyRxgfDyQUYe%22%2C%22signature%22%3A%22ID5_Aee-6icAlfo1z2r7DkmWWHovWH98LNijQ8AlL5Wd99CEWR9Pfwkfl01cE5_SIwAPNKQm9F0kdt84NKoaJlbuyJo%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; _ga=GA1.2.1247685865.1623723739; __gads=ID=7c8f771ce9284ebc:T=1623816827:S=ALNI_MZq8bpHYDnT-u32y0PaxE3hWZQuMw; cto_bidid=p2Ie919udVdHWiUyQnNpaWduOGlyRFRnTzhCMXhFelpneDdFeVBLM2xUR1Yyd3JyTHNxTUtocFR0RkhKT3JYJTJCbUxjWUxOdXhReFFJQ3JZcHZod2FiWEglMkIxTm9YRFJMaSUyRmxjNTdVSDV2cjB5TVc2WE5RJTJGejdRekdQYTRMd2x1WjkxOEJjMW4; cto_bundle=vk6NfF9VUUpSSmhPSkZ6ZGN6Q2twZjU5eDZrQnowU3FnQ2xsTDVnc3hicmVJU2llRlJpUGp1eUVXN0NCMUJSSXZGUHFKaXBpVm5NVHFENm9JMm16VHEybnhoR1k0cjlvM3JiM1hJVG14V3dVam8xRGxpcXpERFZDMmc1cEdtV0lYbEFVS1JTM1E1RnVDOFFEQmVKT21YR2NNTEElM0QlM0Q; hh=969; ww=1344; JSESSIONID=02EC7E8E7D0F07E96AC14C9046CA3AF4; __asc=90123ff317a15bd38f818a6ef1f; _gat_gtag_UA_15537057_1=1; __atuvc=237%7C24; __atuvs=60ca2c58227e3aed003',
            }
            while True:
                try:
                    response2 = requests.get(url2, headers=headers2,timeout=10,proxies=proxies)
                    break
                except Exception as e:
                    # print(e)
                    # print("looping page")
                    time.sleep(random.choice(random_sleep))
                    continue
            html2 = response2.text
            soup2 = BeautifulSoup(html2, 'html.parser')
            divs2 = soup2.findAll("td", attrs={"style": "word-wrap: break-word;"})
            # try :
            #     page = soup2.find("div", attrs={"style": "float:right;"}).find("a")
            # except:
            #     break
            if "Posted by" not in html2:
                break

            if j==1:
                titles = soup2.find("span", attrs={"style": "font-size:16px;"})
                title = titles.get_text()
                title_url = base_link + titles.find("a").attrs.get("href")






                result = {
                    "title": str(title),
                    "title_url": str(title_url),
                    "url" : url2

                }

            user_comments21= user_comments(divs2,url2)


            result["user_comments_page"+str(j)] = user_comments21

            if save_comment == result["user_comments_page"+str(j)]["user_comments"][0]["comment"]:
                break

            save_comment = result["user_comments_page" + str(j)]["user_comments"][0]["comment"]
            # if j==10:
            #     break
            print("page :" + str(i))
            print("forum ke- : " + str(z))
            print("page_forum :" + str(j))

            print(daily_page)
            fields = ['title', 'title_url', 'page_url', 'comment_name', 'comment_time', 'converted_time', 'comment']
            if not daily_page and j == 1:
                with open("/news_cn/requests/KLSE_i3vestor/stock/daily2/" + name_file + ".csv", "w", encoding='utf-8', newline="") as f:
                    write = csv.writer(f, quoting=csv.QUOTE_ALL)
                    write.writerow(fields)
                    f.close()

            for user_comment21 in user_comments21["user_comments"]:
                list =[title, title_url, url2, user_comment21['name'], user_comment21['comment_time'], user_comment21['converted_time'], user_comment21['comment']]
                with open("/news_cn/requests/KLSE_i3vestor/stock/daily2/" + name_file + ".csv", 'a', encoding='utf-8') as f_object:
                    # print(user_comment21['name'])
                    # Pass this file object to csv.writer()
                    # and get a writer object
                    writer_object = writer(f_object)

                    # Pass the list as an argument into
                    # the writerow()
                    # print(str(list).encode("ascii","ignore").decode())

                    writer_object.writerow(list)

                    # Close the file object
                    f_object.close()
        with open("/home/crawler/KLSE_i3vestor/page_daily/last_page_" + name_file +  ".txt", 'w', encoding='utf8') as outfile:
            outfile.write(str(j))

            # if page == None:
            #     break


        # result_all.append(result)
        # name_file = hashlib.md5(title.encode('utf-8')).hexdigest().upper()
        # with open("/home/KLSE_i3vestor2/stock/" + name_file + ".json", 'w', encoding='utf8') as outfile:
        #     json.dump(result_all, outfile, ensure_ascii=False)
        #
        # del result_all[:]


        # if z == 2:
        #     break
    #     #     break
    #     # break
    #
    # break

# result["user_comments"] = user_comments



# print(result)
#         # y=y+1
#         # if y==30:
#         #     break
#     print(i)
# print(result)

# aw=json.loads(str(user_comments))
# print(aw)

