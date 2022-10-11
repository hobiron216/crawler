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


url = "https://www.orientaldaily.com.my/news/society?page=2"
proxy = {"http":"http://ProXy:Rahas!@2020@139.59.105.3:53128"}
response = requests.get(url,proxies=proxy)
status_code = response.status_code
print(response.status_code)
print(response.text)

# url = "https://www.orientaldaily.com.my/news/society?page="
# page1 = str(url)+str(1)
# response = requests.get(page1)
# status_code = response.status_code
# page = 1
# while status_code == 200 and page <= 5:
# 	link = str(url)+str(page)
# 	print(link)
# 	sleep(randint(1,10))
# 	response = requests.get(link)
# 	today = date.today()
# 	print(response.status_code)
# 	print(response.text)

	#---------save index html------------#
# 	filename_index = "/home/amel/orientaldaily/html/index/{}/society/index_{}.html".format(today,hash(link))
# 	os.makedirs(os.path.dirname(filename_index), exist_ok=True)
# 	with open(filename_index, 'w', encoding = 'utf_8_sig') as f:
# 		f.write(str(response.text))

# 	#---------parse html index from url title to req detail html-----------#
# 	soup = bs4.BeautifulSoup(response.content, 'html.parser')
# 	title_link = []
# 	for index in soup.find_all('a',class_='link'):
# 		title = index.get('title')
# 		link = index.get('href')
# 		title_link.append(link)
# # print(title_link)

# 	#------looping title in index html to get detail html-------#
# 	for tl in title_link:
# 		try :
# 			sleep(randint(5,10))
# 			response_detail = requests.get(tl)

# 	#---------parsing url, title, date, article to json--------#
# 			sp_detail = bs4.BeautifulSoup(response_detail.content,"html.parser")
# 			detail_title = sp_detail.title.text
# 			# print(detail_title)
# 			detail_url = sp_detail.find("meta",  property="og:url")['content']
# 			# print(detail_url)
# 			sub_date = detail_url.split('/')
# 			detail_date = sub_date[5]+'-'+sub_date[6]+'-'+sub_date[7]
# 			detail_id = sub_date[8]
# 			# print(detail_date)
# 			detail_article = sp_detail.select('.article.story>p')
# 		# 	print(detail_article)
# 			json_data = {'title':detail_title, 'url':detail_url, 'date':detail_date,'article':detail_article}
# 			# dict_data.append(json_data)

# 		#---------save detail html------------#
# 			filename_content = "/home/amel/orientaldaily/html/content/{}/society/detail_{}.html".format(today,hash(detail_url))
# 			os.makedirs(os.path.dirname(filename_content), exist_ok=True)
# 			with open(filename_content, 'w', encoding = 'utf_8_sig') as f:
# 				f.write(str(response_detail.text))

# 	#-----------save detail json-------------#
# 			filename_json = "/home/amel/orientaldaily/json/content/{}/society/detail_{}.json".format(today,hash(detail_url))
# 			os.makedirs(os.path.dirname(filename_json), exist_ok=True)
# 			with codecs.open(filename_json, 'w',encoding="utf_8_sig") as f:
# 				f.write(str(json_data))
# 		except:
# 			print("skip : " + tl)
	# page=page+1	
# print("End")
