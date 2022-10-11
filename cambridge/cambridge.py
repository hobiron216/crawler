import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import random
import time

Path("/dataph/one_time_crawling/home/cambridge/html/").mkdir(parents=True,exist_ok=True)
Path("/dataph/one_time_crawling/home/cambridge/json/").mkdir(parents=True,exist_ok=True)
i=0
user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
cookies = {
    'XSRF-TOKEN': 'bccd2d95-a10b-4927-b4db-acf00aac70f7',
    'preferredDictionaries': 'english,british-grammar,english-spanish,spanish-english',
    '_ga': 'GA1.3.326148074.1643354853',
    '_gid': 'GA1.3.341892189.1643354853',
    '_pbjs_userid_consent_data': '3524755945110770',
    '_sharedID': '184c2d4b-97ba-4538-a500-6b9fa181f52d',
    'amp-access': 'amp-70sjFjkYmzcsZM630bIlVA',
    '_fbp': 'fb.1.1643354854935.1376512578',
    '__gads': 'ID=e7a6a3e2dcc67a47:T=1643354855:S=ALNI_Mbv4wGX1foi7fSFJW1zqm5OSKJvDA',
    '_lr_env_src_ats': 'false',
    'pbjs-unifiedid': '%7B%22TDID%22%3A%22d40d0dcf-a8c7-4cce-b709-473deba7a832%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-12-28T07%3A27%3A38%22%7D',
    'loginPopup': '6',
    'ssc': '5',
    'OptanonAlertBoxClosed': '2022-01-28T07:32:01.118Z',
    'pageViewCountCurrentSession': '9',
    'pageViewCount': '9',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Jan+28+2022+14%3A32%3A02+GMT%2B0700+(Indochina+Time)&version=6.27.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=ID%3BJK',
    'cto_bundle': 'NME8yF9yMDVnWUpzYnYzeXJLWG1zNU1EVG5xMEhwSmVJd1k5bVUlMkJpaHF2VklKVlBIaiUyRmVXYjFQbzdtaCUyQlhVZWV1eGNIMDNqM1dUUGVVV0VrVWdPb28lMkJhJTJGdTJpNmtwT005ZURXJTJGcFkzN2I0enFLeWZUMjhQVUlLdDhySXdESW5SaklURnlDRERJaCUyQjRIVjUyWElBUW0zbmw5QSUzRCUzRA',
    'cto_bidid': 'BfHSDV8lMkJLUVAlMkJwSEs2aEl4TiUyQktIQW5Kalg5Z0NVZVZWeXh1RktsN3NMU0x6U2QxcFdWcUgyNnNSWG9UdG85amdHRHc0blFsblJSUVlVR3RpVVllSUFjUGolMkJyMGNnZmxJWHJBJTJCVTE4bWxvWUNwb0UlM0Q',
}
data = []
proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
with open("cambridge_text.json", 'r', encoding='utf_8_sig') as outfile:
    list_url = json.load(outfile)

    for text in list_url:

        if text:
            user_agent = random.choice(user_agents)
            headers = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            }
            while True:
                try:
                    response = requests.get('https://dictionary.cambridge.org/dictionary/english/' + str(text).strip(), headers=headers, proxies=proxies, timeout=5)
                    break
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    continue

            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            try:
                type = soup.find("span", class_="pos dpos").get_text().strip()
            except:
                type = ""

            result = {
                "word" : text,
                "type" : type
            }
            i = i + 1
            print(i)
            print(len(list_url))
            # if i>10:
            #     break
            with open("/dataph/one_time_crawling/home/cambridge/html/" + text + ".html",'w',encoding='utf8') as outfile:
                outfile.write(str(soup))
            data.append(result)



with open("/dataph/one_time_crawling/home/cambridge/json/cambridge_dictionary.json", 'w', encoding='utf_8_sig') as outfile:
    json.dump(data, outfile, ensure_ascii=False)