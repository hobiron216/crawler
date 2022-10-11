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
import re
from datetime import date
from datetime import datetime
import sys

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

with open("/home/amel/enanyang/check_first_url_global_anti-epidemic.json", 'r', encoding='utf_8_sig') as outfile:
  first_url= json.load(outfile)
list_url = []

data=0
url = "https://www.enanyang.my/api/get/term/articles/3216?page=" ##news=11
page1 = str(url)+str(1)
response = requests.get(url)
status_code = response.status_code
# print(status_code)
# print(response.content)
page = 0
while status_code == 200 and page <= 5:
	link = str(url)+str(page)
# 	# print(link)
	sleep(randint(1,10))
	response = requests.get(link)
	response = response.content
	jsonStr = json.loads(response)
	date = date.today()
	hours = datetime.now().strftime("%H")  
	# print(jsonStr)

	#---------save index html------------#
	filename_index = "/home/amel/enanyang/json/index/{}/{}/global_anti-epidemic/index_{}.json".format(date,hours,hash(link))
	os.makedirs(os.path.dirname(filename_index), exist_ok=True)
	with open(filename_index, 'w', encoding = 'utf_8_sig') as f:
		f.write(str(jsonStr))

	##-------------get detail------------##
	for j in jsonStr :
		# try :
		url_detail = "https://www.enanyang.my" + j['link']
		print("url detail : "+url_detail)
		print("first url : "+first_url)
		if url_detail in first_url:
			message = "Engine : Enanyang  \n" + "Category : global_anti-epidemic-hourly \n" +  "Data : " + str(data)
			telegram_bot_sendtext(str(message))
			sys.exit("EXIT : url == first url")
		else :
			print("url != first url")				
		response_detail = requests.get(url_detail)
		# print(response_detail.content)
		nid = j['nid']

		##---------parsing url, title, date, article to json--------##
		sp_detail = bs4.BeautifulSoup(response_detail.content,"html.parser")
		detail_title = sp_detail.title.text
		# print("Title detail : " + detail_title)
		detail_url = sp_detail.find("meta",  property="og:url")['content']
		# print("Url detail : " + detail_url)
		detail_date = sp_detail.find("div", class_="ttr-post-date").text
		detail_date = detail_date.strip()
		detail_date = re.sub('[^a-zA-Z0-9 \n\.]', '', detail_date)
		# print("Date detail : " + str(detail_date))
		detail_article = sp_detail.select('.paragraph.paragraph--type--text.paragraph--view-mode--default>p')
		# print(str(detail_article))
		json_data = {'title':detail_title, 'url':detail_url, 'date':str(detail_date),'article':str(detail_article)}
		# print(json_data)

		list_url.append(url_detail)

		##-------save detail html-------##
		filename_content = "/home/amel/enanyang/html/content/{}/{}/global_anti-epidemic/detail_{}.html".format(date,hours,hash(detail_url))
		os.makedirs(os.path.dirname(filename_content), exist_ok=True)
		with open(filename_content, 'w', encoding = 'utf_8_sig') as f:
			f.write(str(response_detail.text))

		##-----------save detail json-------------##
		filename_json = "/home/amel/enanyang/json/content/{}/{}/global_anti-epidemic/detail_{}.json".format(date,hours,hash(detail_url))
		os.makedirs(os.path.dirname(filename_json), exist_ok=True)
		with codecs.open(filename_json, 'w',encoding="utf_8_sig") as f:
			f.write(str(json_data))
			data = data + 1
		# except:
		# 	print("skip : " + tl)
	page=page+1

# message = "Engine : Enanyang  \n" + "Category : global_anti-epidemic-hourly \n" +  "Data : " + str(data)
# telegram_bot_sendtext(str(message))

with codecs.open("/home/amel/enanyang/check_first_url_global_anti-epidemic.json", 'w',encoding="utf_8_sig") as l:
  json.dump(list_url[0],l,ensure_ascii=False)