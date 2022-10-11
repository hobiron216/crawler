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

url = "https://www.enanyang.my/api/get/term/articles/11?page=" ##international=11
page1 = str(url)+str(1)
response = requests.get(url)
status_code = response.status_code
# print(status_code)
# print(response.content)
page = 1
while status_code == 200 :
	link = str(url)+str(page)
# 	# print(link)
	sleep(randint(1,10))
	response = requests.get(link)
	response = response.content
	jsonStr = json.loads(response)
	# print(jsonStr)

	#---------save index html------------#
	with open("/home/amel/enanyang/international/index_{}.json".format(page), 'w', encoding = 'utf_8_sig') as f:
		f.write(str(jsonStr))

	##-------------get detail------------##
	for j in jsonStr :
		try :
			url_detail = "https://www.enanyang.my" + j['link']
			response_detail = requests.get(url_detail)
			# print(response_detail.content)
			nid = j['nid']

			##---------parsing url, title, date, article to json--------##
			sp_detail = bs4.BeautifulSoup(response_detail.content,"html.parser")
			detail_title = sp_detail.title.text
			print("Title detail : " + detail_title)
			detail_url = sp_detail.find("meta",  property="og:url")['content']
			print("Url detail : " + detail_url)
			detail_date = sp_detail.find("div", class_="ttr-post-date").text
			detail_date = detail_date.strip()
			detail_date = re.sub('[^a-zA-Z0-9 \n\.]', '', detail_date)
			print("Date detail : " + str(detail_date))
			detail_article = sp_detail.select('.paragraph.paragraph--type--text.paragraph--view-mode--default>p')
			print(str(detail_article))
			json_data = {'title':detail_title, 'url':detail_url, 'date':str(detail_date),'article':str(detail_article)}
			print(json_data)

			##-------save detail html-------##
			with open("/home/amel/enanyang/international/detail_{}_{}.html".format(page, nid), 'w', encoding = 'utf_8_sig') as f:
				f.write(str(response_detail.text))

			##-----------save detail json-------------##
			with codecs.open("/home/amel/enanyang/international/detail_{}_{}.json".format(page, nid), 'w',encoding="utf_8_sig") as f:
				f.write(str(json_data))
		except:
			print("skip : " + url_detail)
	page=page+1	
# print("End")
