import requests
from bs4 import BeautifulSoup
from datetime import date
from pathlib import Path
import hashlib
import json
import random
import time

import datetime as datetime21

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

site_name="kpkesihatan"
page=0
today = date.today()
crawl_date = today.strftime("%Y%m%d")
# crawl_date = today.strftime("20211031")
today_news = date.today() - datetime21.timedelta(1)
crawl_date_news = today_news.strftime("%Y/%m/%d")
path= "/news_cn/requests/"
Path(path + site_name + "/html/" + crawl_date + "/").mkdir(parents=True,exist_ok=True)
Path(path + site_name + "/json/"  + crawl_date + "/").mkdir(parents=True,exist_ok=True)
user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
a=True
data=0
while a :
    page=page+1
    url = "https://kpkesihatan.com/page/" + str(page) + "/"

    user_agent = random.choice(user_agents)
    time.sleep(1)
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "en-US,en;q=0.9,id;q=0.8",
        'cache-control': "no-cache",
        'connection': "keep-alive",

        'upgrade-insecure-requests': "1",
        'user-agent': user_agent,
        'cookie': 'ncbi_sid=CE899787D9195471_2562SID; pmc.article.report=; _ga=GA1.2.1661002836.1569822027; entrezSort=pmc:; _gid=GA1.2.2059851631.1569998064; WebEnv=1zGUsr%40CE899787D9195471_2562SID; _gat_ncbiSg=1; _gat_dap=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAc+AzPgAwDsAIgJwAstAQtqQIynsccBsLlpRDLgDoAtnACsIADQgArgDsANgHsAhqnlQAHgBdMoAEyZwIgMbSQRY2DMXaxncvMzJWAPTIAzp9lRPbogNWciI3Cy5jaFNlCHQZIOM8fEoAQVoDKjpxMgM2Tk58Ay5SWnxxUQkLXOszDBtTDEcGj29ff0Dg0KqjLAB3fqF5UwAjZEHFEUHkRCEAc2UYKupjFiIuCJkiUmNyLnwLIhYVraPNnpByegOrLAAzVUVPKAP7LB0IXwP9rAPlrHJqGxAfsZLRtv9ASwWNRyHYbiBSEIikJTiArlgFCp1JpdHZXCBUeJ4atWBZxK8CdRJC4Ilhti5YXTwkd/iAAL5soA'
    }
    while True:
        try:
            r= requests.get(url, headers, timeout=10)
            break
        except:
            continue
    html=r.text

    if "Error 404" in html:
        break
    soup =BeautifulSoup (html,'html.parser')

    divs = soup.findAll("article", class_="post-archive")

    for div in divs:
        link = div.find("a").attrs.get("href")

        if "situasi-semasa" not in link:
            continue


        if crawl_date_news in str(link):

            # print(link)
            # continue
            user_agent = random.choice(user_agents)
            time.sleep(1)
            headers = {
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                'accept-encoding': "gzip, deflate",
                'accept-language': "en-US,en;q=0.9,id;q=0.8",
                'cache-control': "no-cache",
                'connection': "keep-alive",

                'upgrade-insecure-requests': "1",
                'user-agent': user_agent,
                'cookie': 'ncbi_sid=CE899787D9195471_2562SID; pmc.article.report=; _ga=GA1.2.1661002836.1569822027; entrezSort=pmc:; _gid=GA1.2.2059851631.1569998064; WebEnv=1zGUsr%40CE899787D9195471_2562SID; _gat_ncbiSg=1; _gat_dap=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIFEAc+AzPgAwDsAIgJwAstAQtqQIynsccBsLlpRDLgDoAtnACsIADQgArgDsANgHsAhqnlQAHgBdMoAEyZwIgMbSQRY2DMXaxncvMzJWAPTIAzp9lRPbogNWciI3Cy5jaFNlCHQZIOM8fEoAQVoDKjpxMgM2Tk58Ay5SWnxxUQkLXOszDBtTDEcGj29ff0Dg0KqjLAB3fqF5UwAjZEHFEUHkRCEAc2UYKupjFiIuCJkiUmNyLnwLIhYVraPNnpByegOrLAAzVUVPKAP7LB0IXwP9rAPlrHJqGxAfsZLRtv9ASwWNRyHYbiBSEIikJTiArlgFCp1JpdHZXCBUeJ4atWBZxK8CdRJC4Ilhti5YXTwkd/iAAL5soA'
            }
            while True:
                try:
                    r2= requests.get(link, headers=headers, timeout=10)
                    break
                except:
                    continue

            html2 = r2.text
            soup2 = BeautifulSoup(html2, 'html.parser')

            # date= soup2.find("strong").get_text()
            body= soup2.find("body").get_text()
            ndate = soup2.find("meta", property="article:published_time")['content']
            ndate = ndate.split("T")
            ndate = ndate[0]

            # contents = soup2.find("section", class_="entry").get_text().split("\nShare")
            # content = contents[0]
            contents = soup2.find("section", class_="entry").findAll("p")
            content = ""
            z=0
            for content21 in contents:
                z=z+1
                # print("wwkwkwk")
                # stop =  content21.find("strong")
                # print(stop)
                if z>3:
                    continue

                content = content + content21.get_text().strip()

            contents2 = soup2.find("ul").find_next("ul").findAll("li")

            for content2 in contents2:
                # print(content2.get_text())
                content = content + content2.get_text().strip()


            href21 = hashlib.md5(link.encode('utf-8')).hexdigest().upper()
            path_html = path + site_name  + "/html/" + crawl_date + "/" + href21 + ".html"
            result = {
                "ndate": ndate,
                "content": content,
                "sitename": site_name,
                "path_html": path_html,
                "url": link,
                "body" : body,
                "crawl_date" : crawl_date
            }

            with open(path + site_name + "/html/" + crawl_date + "/" + href21 +  ".html", 'w',
                      encoding='utf8') as outfile:
                outfile.write(str(soup2))
            with open(path + site_name + "/json/" + crawl_date + "/"  + href21 + ".json", 'w',
                      encoding='utf_8_sig') as outfile:
                json.dump(result, outfile, ensure_ascii=False)

            print("page :" + str(page))
            data=data+1
            print("data : " + str(data))
        else:
            if page==2:
                a=False
                break
    #     break
    # break
message = "Engine : kpkesihatan \n" + "Data : " + str(data)
telegram_bot_sendtext(str(message))