import time
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from pathlib import Path


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
cookies = {
    'PHPSESSID': 'u7bjemmk59auqol4mb3vgc8mhm',
    '_csrf': '4b932623df5abdc1c1239520eed7d68399ac611edd346362d29b9d985ce19145a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22FasFJ-HsYnXhrdFjSPAcRwE3wt-T_BoH%22%3B%7D',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
}
while True:
    try:
        response = requests.get('http://infobencanajkmv2.jkm.gov.my/portal/index', headers=headers, cookies=cookies, timeout=10)
        break
    except requests.exceptions.RequestException as e:
        print("connetion timeout index")
        continue

html = response.text
soup = BeautifulSoup(html,'html.parser')
divs = soup.findAll("div", class_="col-sm-6 p-w-md")
jumlah_pusat_buka = soup.find("p", id="pusat-buka").get_text().replace(r"\n","").strip()
jumlah_negeri = soup.find("p", id="jumlah-negeri").get_text().replace(r"\n","").strip()
jumlah_keluarga = soup.find("p", id="jumlah-keluarga").get_text().replace(r"\n","").strip()
jumlah_mangsa = soup.find("p", id="jumlah-mangsa").get_text().replace(r"\n","").strip()

data=[]
result_banjir = {}
result2={
    "jumlah_pusat_buka" : jumlah_pusat_buka,
    "jumlah_negeri" : jumlah_negeri,
    "jumlah_keluarga" : jumlah_keluarga,
    "jumlah_mangsa" : jumlah_mangsa
}
result_banjir["banjir"] = result2


for div in divs:
    city = div.find("h2").get_text()
    data_tabels = div.findAll("strong")
    loop_tabel=0
    for data_tabel in data_tabels:
        loop_tabel = loop_tabel + 1
        if loop_tabel==1:
            pusat_buka = data_tabel.get_text().replace("Pusat Buka", "").strip()
        elif loop_tabel==2:
            mangsa = data_tabel.get_text()
        elif loop_tabel==3:
            keluarga = data_tabel.get_text()
        elif loop_tabel==4:
            lelaki_dewasa = data_tabel.get_text()
        elif loop_tabel==5:
            perempuan_dewasa = data_tabel.get_text()
        elif loop_tabel==6:
            kanak_kanak_lelaki = data_tabel.get_text()
        elif loop_tabel==7:
            kanak_kanak_perempuan = data_tabel.get_text()
        elif loop_tabel==8:
            bayi_lelaki = data_tabel.get_text()
        elif loop_tabel==9:
            bayi_perempuan = data_tabel.get_text()
        elif loop_tabel==10:
            warga_emas_lelaki = data_tabel.get_text()
        elif loop_tabel==11:
            warga_emas_perempuan = data_tabel.get_text()
        elif loop_tabel==12:
            oku_lelaki = data_tabel.get_text()
        elif loop_tabel==13:
            oku_perempuan = data_tabel.get_text()

    result= {
        "city" : city,
        "pusat_buka" : pusat_buka,
        "mangsa" : mangsa,
        "keluarga" : keluarga,
        "lelaki_dewasa" : lelaki_dewasa,
        "perempuan_dewasa" : perempuan_dewasa,
        "kanak_kanak_lelaki" : kanak_kanak_lelaki,
        "kanak_kanak_perempuan" : kanak_kanak_perempuan,
        "bayi_lelaki" : bayi_lelaki,
        "bayi_perempuan" : bayi_perempuan,
        "warga_emas_lelaki" : warga_emas_lelaki,
        "warga_emas_perempuan" : warga_emas_perempuan,
        "oku_lelaki" : oku_lelaki,
        "oku_perempuan" : oku_perempuan

    }
    result_banjir[city] = result

# print(data)
today = date.today()
crawl_date = today.strftime("%Y%m%d")
Path("/dataph/one_time_crawling/home/info_bencana_jkm/" + crawl_date + "/" ).mkdir(parents=True, exist_ok=True)
with open('/dataph/one_time_crawling/home/info_bencana_jkm/' + crawl_date + '/general_data.json', 'w', encoding='utf_8_sig') as outfile:
    json.dump(result_banjir, outfile, ensure_ascii=False)

message = "Engine : jkm-general"
telegram_bot_sendtext(str(message))
# data21 = data21 + 1
# print("total_data : " + str(data21))
# print("category : "  + category)
# print("total_count : " +  str(total_count))

# open(r'E:\job3.pdf', 'wb').write(response.content)
# with open(r'E:\tes_futerejob.json', 'w', encoding='utf_8_sig') as outfile:
#     json.dump(data,outfile)



