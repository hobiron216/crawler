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

def detail(divs2):
    data = []
    for div2 in divs2:
        id = div2.attrs.get("data-id")

        disrict = div2.find("b").get_text()
        address = div2.find("small").get_text()
        kapasiti = div2.find("td", class_="text-center label label-warning").get_text().replace("Kapasiti", "").strip()

        cookies = {
            'PHPSESSID': 'u7bjemmk59auqol4mb3vgc8mhm',
            '_csrf': '4b932623df5abdc1c1239520eed7d68399ac611edd346362d29b9d985ce19145a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22FasFJ-HsYnXhrdFjSPAcRwE3wt-T_BoH%22%3B%7D',
        }

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'X-CSRF-Token': 'IddX35vyX2oPL6TcTdkHBAbKNTy2pLPKYkGJeAr7KeVntiSZ0d8XGVZB_LQ_vUFuVZp0X-TT9vkVNaQsVblGrQ==',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://infobencanajkmv2.jkm.gov.my',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://infobencanajkmv2.jkm.gov.my/portal/index',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        }
        data21 = {
            'id': id
        }

        while True:
            try:
                response = requests.post('http://infobencanajkmv2.jkm.gov.my/portal/get-details-mangsa-bencana',
                                         headers=headers, cookies=cookies, data=data21, timeout=10)
                break
            except requests.exceptions.RequestException as e:
                print("connetion timeout id")
                continue
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data_tables = soup.find("tr")
        data_table = data_tables.find("td").get_text().replace("<\/td>", "").replace("<\/td>", "").replace(r"<\/tr>\n",
                                                                                                           r"\n")
        data_table = data_table.strip().split(r"\n")

        jumlah_keluarga = data_table[1].strip()
        dewasa_lelaki = data_table[5].strip()
        dewasa_perempuan = data_table[6].strip()
        kanak_kanak_lelaki = data_table[10].strip()
        kanak_kanak_perempuan = data_table[11].strip()
        bayi_lelaki = data_table[15].strip()
        bayi_perempuan = data_table[16].strip()
        warga_emas_lelaki = data_table[20].strip()
        warga_emas_perempuan = data_table[21].strip()
        oku_lelaki = data_table[25].strip()
        oku_perempuan = data_table[26].strip()
        bukan_warganegara_dewasa_lelaki = data_table[30].strip()
        bukan_warganegara_dewasa_perempuan = data_table[31].strip()
        bukan_warganegara_kanak_kanak = data_table[35].strip()
        bukan_warganegara_bayi = data_table[39].strip()

        result = {
            "city" : city,
            "disrict": disrict,
            "address": address,
            "kapasiti": kapasiti,
            "jumlah_keluarga": jumlah_keluarga,
            "dewasa_lelaki": dewasa_lelaki,
            "dewasa_perempuan": dewasa_perempuan,
            "kanak_kanak_lelaki": kanak_kanak_lelaki,
            "kanak_kanak_perempuan": kanak_kanak_perempuan,
            "bayi_lelaki": bayi_lelaki,
            "bayi_perempuan": bayi_perempuan,
            "warga_emas_lelaki": warga_emas_lelaki,
            "warga_emas_perempuan": warga_emas_perempuan,
            "oku_lelaki": oku_lelaki,
            "oku_perempuan": oku_perempuan,
            "bukan_warganegara_dewasa_lelaki": bukan_warganegara_dewasa_lelaki,
            "bukan_warganegara_dewasa_perempuan": bukan_warganegara_dewasa_perempuan,
            "bukan_warganegara_kanak_kanak": bukan_warganegara_kanak_kanak,
            "bukan_warganegara_bayi": bukan_warganegara_bayi
        }
        data.append(result)

    return data
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
divs = soup.findAll("div", class_="card")
data={}
a=0
for div in divs:
    a=a+1
    # if a>2:
    #     break
    # print(div)
    divs2 = div.findAll("tr")
    city = div.find("h4").get_text().replace(r"\n","").strip()

    result_detail = detail(divs2)

    data[city] = result_detail
    # break

today = date.today()
crawl_date = today.strftime("%Y%m%d")
Path("/dataph/one_time_crawling/home//info_bencana_jkm/" + crawl_date + "/" ).mkdir(parents=True, exist_ok=True)
with open('/dataph/one_time_crawling/home//info_bencana_jkm/' + crawl_date + '/detail_data.json', 'w', encoding='utf_8_sig') as outfile:
    json.dump(data, outfile, ensure_ascii=False)

message = "Engine : jkm-detail"
telegram_bot_sendtext(str(message))