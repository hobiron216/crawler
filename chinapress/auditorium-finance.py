import requests
import json 
import time
import bs4
from lxml import html
import uuid
import codecs
from random import randint
from time import sleep
import os
from datetime import date
import sys, os
def telegram_bot_sendtext(bot_message):
	global response
	bot_token = '1603186460:AAFaH_UjuERmIYthGcWWDeS80U7CRmWwpq4'
	bot_chatID = '-597807195'
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

	while True:
		try:
			response = requests.get(send_text, timeout=10)
			break
		except requests.exceptions.RequestException as e:
			print("gagal kirim telegram")
			continue

	return response.json()

list_url = []

data=0
url = "https://www.chinapress.com.my/category/%e8%af%84%e8%ae%ba/page/" #auditorium-finance
page1 = str(url)+str(1)+str("/?gpid=537706")
proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
import random
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
# while True:
# 	try:
# 		response = requests.get(page1, proxies=proxies, headers=headers)
# 		if response.status_code==200:
# 			break
# 	except:
# 		continue
response = requests.get(page1, proxies=proxies, headers=headers)
status_code = response.status_code
page = 1
while status_code == 200 and page <= 20:
	link = str(url)+str(page)+str("/?gpid=540877")
	print(link)
	sleep(randint(1,10))
	response = requests.get(link, proxies=proxies, headers=headers)
	today = date.today()
	# print(response.status_code)

#---------save index html------------#
	filename_index = "/home/amel/chinapress/html/index/{}/auditorium-finance/index_{}.html".format(today,hash(link))
	os.makedirs(os.path.dirname(filename_index), exist_ok=True)
	with open(filename_index, 'w', encoding = 'utf_8_sig') as f:
		f.write(str(response.text))

	#---------parse html index from url title to req detail html-----------#
	soup = bs4.BeautifulSoup(response.content, 'html.parser')
	# print(soup)
	title_link = []
	for a in soup.select('.title a'):
		link_detail = a['href']
		title_link.append(link_detail)
	# print(title_link)

#------looping title in index html to get detail html-------#
	for tl in title_link:
		try :
			sleep(randint(5,10))
			response_detail = requests.get(tl, proxies=proxies, headers=headers)

	#---------parsing url, title, date, article to json--------#
			sp_detail = bs4.BeautifulSoup(response_detail.content,"html.parser")
			detail_title = sp_detail.title.text
			detail_title = detail_title.split('|')[0]
			# print('Title : ' + detail_title)
			detail_url = sp_detail.find("meta",  property="og:url")['content']
			# print('Url : ' + detail_url)
			sub_date = detail_url.split('/')[-3]
			# print('Date : ' + sub_date)
			detail_article = sp_detail.select('.entry-content.clearfix>p')
			# print(str(detail_article))
			detail_id = sp_detail.find('div', id='post_id').text
			# print(detail_id)
			json_data = {'title':detail_title, 'url':detail_url, 'date':sub_date,'article':str(detail_article)}
			# print(str(json_data))
			list_url.append(tl)

		#---------save detail html------------#
			filename_content = "/home/amel/chinapress/html/content/{}/auditorium-finance/detail_{}.html".format(today,hash(detail_url))
			os.makedirs(os.path.dirname(filename_content), exist_ok=True)
			with open(filename_content, 'w', encoding = 'utf_8_sig') as f:
				f.write(str(response_detail.text))

	#-----------save detail json-------------#

			filename_json = "/home/amel/chinapress/json/content/{}/auditorium-finance/detail_{}.json".format(today,hash(detail_url))
			os.makedirs(os.path.dirname(filename_json), exist_ok=True)
			with codecs.open(filename_json, 'w',encoding="utf_8_sig") as f:
				f.write(str(json_data))
				data = data + 1
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print("skip : " + tl)
	page=page+1

message = "Engine : Chinapress  \n" + "Category : auditorium-finance \n" +  "Data : " + str(data)
telegram_bot_sendtext(str(message))

with codecs.open("/home/amel/chinapress/check_url_auditorium_finance.json", 'w',encoding="utf_8_sig") as l:
  json.dump(list_url,l,ensure_ascii=False)