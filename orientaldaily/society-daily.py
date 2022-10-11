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

url = "https://www.orientaldaily.com.my/news/society?page="
proxy = {"http":"http://ProXy:Rahas!@2020@139.59.105.3:53128"}
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection': 'keep-alive',
'Host': 'www.orientaldaily.com.my',
'Referer': 'https://www.orientaldaily.com.my/news/society?page=2',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

page1 = str(url)+str(1)
print(page1)
while True:
	try :
		response = requests.get(page1,proxies=proxy,headers=headers, timeout=10)
		break
	except requests.exceptions.RequestException as e:
		print("loop : " + page1)
		continue
status_code = response.status_code
print(status_code)
page = 1
while status_code == 200 and page <= 15:
	link = str(url)+str(page)
	# print(link)
	sleep(randint(1,10))
	while True:
		try:
			response = requests.get(link,proxies=proxy, timeout=10)
			break
		except requests.exceptions.RequestException as e:
			print("loop : " + link)
			continue
	today = date.today()
	# print(response.status_code)

	#---------save index html------------#
	filename_index = "/home/amel/orientaldaily/html/index/{}/society/index_{}.html".format(today,hash(link))
	os.makedirs(os.path.dirname(filename_index), exist_ok=True)
	# with open(filename_index, 'w', encoding = 'utf_8_sig') as f:
	with open(filename_index, 'w', encoding = 'utf-8') as f:
		f.write(str(response.text))

	#---------parse html index from url title to req detail html-----------#
	soup = bs4.BeautifulSoup(response.content, 'html.parser')
	title_link = []
	for index in soup.find_all('a',class_='link'):
		title = index.get('title')
		link = index.get('href')
		title_link.append(link)
	# print(title_link)

	#------looping title in index html to get detail html-------#
	for tl in title_link:
		try :
			sleep(randint(5,10))
			while True:
				try:
					response_detail = requests.get(tl,proxies=proxy, timeout=10)
					break
				except requests.exceptions.RequestException as e:
					# print(e)
					print("loop : " + tl)
					continue

	#---------parsing url, title, date, article to json--------#
			sp_detail = bs4.BeautifulSoup(response_detail.content,"html.parser")
			detail_title = sp_detail.title.text
			# print(detail_title)
			detail_url = sp_detail.find("meta",  property="og:url")['content']
			# print(detail_url)
			sub_date = detail_url.split('/')
			detail_date = sub_date[5]+'-'+sub_date[6]+'-'+sub_date[7]
			detail_id = sub_date[8]
			# print(detail_date)
			detail_article = sp_detail.select('.article.story>p')
		# 	print(detail_article)
			json_data = {'title':detail_title, 'url':detail_url, 'date':detail_date,'article':detail_article}
			# dict_data.append(json_data)

		#---------save detail html------------#
			filename_content = "/home/amel/orientaldaily/html/content/{}/society/detail_{}.html".format(today,hash(detail_url))
			os.makedirs(os.path.dirname(filename_content), exist_ok=True)
			with open(filename_content, 'w', encoding = 'utf-8') as f:
				f.write(str(response_detail.text))

	#-----------save detail json-------------#
			filename_json = "/home/amel/orientaldaily/json/content/{}/society/detail_{}.json".format(today,hash(detail_url))
			os.makedirs(os.path.dirname(filename_json), exist_ok=True)
			with codecs.open(filename_json, 'w',encoding="utf-8") as f:
				f.write(str(json_data))
		except Exception as e:
			print(e)
			print("skip : " + tl)
	page=page+1	
print("End")
