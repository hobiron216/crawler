import requests

cookies = {
    'cookiesession1': '678A3E0DEFGHIJKLMNOPQRSTUVWY37A6',
    'PHPSESSID': '8ha9e4ma50r9h4j1u8a3ec38ns',
    '_ga': 'GA1.2.987928523.1639561740',
    '_gid': 'GA1.2.1613960585.1639561740',
    '_gat_gtag_UA_200691671_1': '1',
    '__atuvc': '2%7C50',
    '__atuvs': '61b9b9d50a44de0c001',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'https://jendela.my',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://jendela.my/',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
}

data = '{"category":"wireless-broadband","address":"47, Jalan Astaka U8/84A, Bukit Jelutong Business And Technology Centre, 40150 Shah Alam, Selangor","x":101.54724508644716,"y":3.104771970331645}'
proxies = {"http": "http://42.1.62.73:8228",
            "https": "https://42.1.62.73:8228",
}
response = requests.post('https://jendela.my/api/Map/GetServiceCoverage', proxies = proxies, headers=headers, cookies=cookies, data=data,  verify=False)
print(response.text)