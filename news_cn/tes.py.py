import hashlib
import json
import requests
from pathlib import Path
# from logger import Logger
from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import random
import time
# import newspaper
url=str("http://www.xinhuanet.com/fortune/2021-03/10/c_1127191927.htm")
# print("url : " + url)
b = True

user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
user_agent = random.choice(user_agents)
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
proxies = { 'https' : 'https://ProXy:Rahas!@2020@139.59.105.3:53128' , 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
i=0
while b:
    try:
        i=i+1
        if i>=5:
            b= False
        r = requests.get(url, timeout=50,  headers=headers, proxies=proxies)
        b = False

    except requests.exceptions.RequestException as e:
        print("connetion timeout")
        continue
r.encoding = 'utf-8'
html = r.text
soup = BeautifulSoup(html, "html.parser")
soup21 = BeautifulSoup(html, "html.parser")

title = soup.find("span", class_="title")
if title == None:
    title = soup.find("div", class_="h-title").get_text()
else :
    title=title.get_text()

article = soup.find("div", id="detail").get_text()
year= soup.find("span", class_="year").get_text().replace("\n","").replace(" ","")
day21 = soup.find("span", class_="day").get_text().replace(" ","")
day21=day21.split("/")


try:
    month=day21[0]
    day=day21[1]
    time21 = soup.find("span", class_="time").get_text().replace(" ", "")
    ndate = year + "-" + month + "-" + day + " " + time21
except:
    month=day21[0].replace("\r\n","")
    day=day21[1].replace("\r\n","")
    ndate = year + "-" + month + "-" + day + " " + "12:00:01"
result = {

                "title": title,
                "article": article,
                "ndate": ndate,


                "url": url

            }
print(result)