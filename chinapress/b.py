import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
request = requests.get("https://www.chinapress.com.my/category/%e8%af%84%e8%ae%ba/page/1?gpid=540877", headers=headers, verify=False)
print(request.text)
