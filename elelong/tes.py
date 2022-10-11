import requests
from bs4 import BeautifulSoup
from selenium import webdriver
url = "https://elelong.kehakiman.gov.my/BidderWeb/Home/Index"
driver = webdriver.Chrome(executable_path=r'C:\chromedriver')
driver.get(url)
cookies21=driver.get_cookies()
c = {c['name']: c['value'] for c in cookies21}
cookies=c

headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://elelong.kehakiman.gov.my',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://elelong.kehakiman.gov.my/BidderWeb/Home/Index',
                'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            }

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
token = soup.find("input").attrs.get("value")
data = {
'__RequestVerificationToken': token,
  'state': '0',
  'priceRange': '0',
  'landUsed': '0',
  'restrictionInInterest': '0',
  'tenure': '0',
  'auctionDate': '',
  'propertyAddress': '',
  'pageIndex': '0',
  'pageSize': '20'
}

print(cookies)
print(data)

response = requests.post('https://elelong.kehakiman.gov.my/BidderWeb/Home/SearchAuction', headers=headers, cookies=cookies, data=data)
print(response.text)
