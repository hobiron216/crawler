import requests
from bs4 import  BeautifulSoup
import hashlib
import requests
from dateutil import parser
import json
from pathlib import Path
import random
import time
from selenium import webdriver
from pyvirtualdisplay import Display

# display = Display(visible=0, size=(1366, 768))
# display.start()

Path("/home/KLSE_i3vestor/news & blogs/").mkdir(parents=True,exist_ok=True)
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
random_sleep= [1,2,3,4,5,6,7,8,9,10]
proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
# browser= webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
def user_comments(divs2,link):
    user_comments=[]

    for div2 in divs2:

        name = div2.find("span", class_="comuid").get_text()
        comment_time = div2.find("span", class_="comdt").get_text()
        try :

            converted_time = str(parser.parse(comment_time)).replace("-", "")
        except:
            converted_time = ""
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
    if i < 712:
        continue
    url = news_url + "&fp=" + str(i)
    print(url)
    user_agent = random.choice(user_agents)
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
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            break
        except:
            continue
    html=response.text

    # browser.get(url)
    # time.sleep(100)
    # html=browser.page_source
    soup = BeautifulSoup(html,'html.parser')


    divs = soup.findAll("td", attrs={"style" : "padding-bottom:10px;word-wrap: break-word;"})
    z=0
    for div in divs:
        z=z+1
        # if i<217:
        #     if z<24:
        #         continue
        if "No discussion entries available." in div:
            break
        link = base_link + div.find("a").attrs.get("href")
        # print("link : " + str(link))
        j=0
        # divs_cadangan=""
        save_comment = ""
        while True:
            time.sleep(random.choice(random_sleep))
            j=j+1
            url2 = link + "?ftp=" + str(j)
            print("link : " + str(url2))
            user_agent2 = random.choice(user_agents)
            headers2 = {
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
            while True:
                try:
                    response2 = requests.get(url2, headers=headers2, timeout=10)
                    break
                except:
                    time.sleep(random.choice(random_sleep))
                    continue
            html2 = response2.text
            # browser.get(url2)
            # time.sleep(3)
            # html2=browser.page_source
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
                }

            user_comments21= user_comments(divs2,url2)


            result["user_comments_page"+str(j)] = user_comments21

            if save_comment == result["user_comments_page"+str(j)]["user_comments"][0]["comment"]:
                break
            # if j==10:
            #     break
            print("page :" + str(i))
            print("forum ke- : " + str(z))
            # divs_cadangan = divs2
            # if page == None:
            #     break
            save_comment = result["user_comments_page"+str(j)]["user_comments"][0]["comment"]

        result_all.append(result)
        name_file = hashlib.md5(title.encode('utf-8')).hexdigest().upper()


        with open("/home/KLSE_i3vestor/news & blogs/" + str(name_file) + ".json", 'w', encoding='utf8') as outfile:
            json.dump(result_all, outfile, ensure_ascii=False)

        del result_all[:]

# browser.close()
# display.stop()

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

