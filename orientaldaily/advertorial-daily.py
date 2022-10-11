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
import random
import traceback

url = "https://www.orientaldaily.com.my/news/advertorial?page="
proxy = {"http":"http://pxuser:r@h@s!@2o2o@159.65.3.103:8252"}
data=0
list_url = []

page1 = str(url)+str(1)
user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
while True:
	user_agent = random.choice(user_agents)
	headers = {
			    'authority': 'www.orientaldaily.com.my',
			    'cache-control': 'max-age=0',
			    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
			    'sec-ch-ua-mobile': '?0',
			    'sec-ch-ua-platform': '"Windows"',
			    'upgrade-insecure-requests': '1',
			    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
			    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			    'sec-fetch-site': 'same-origin',
			    'sec-fetch-mode': 'navigate',
			    'sec-fetch-user': '?1',
			    'sec-fetch-dest': 'document',
			    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
			    'cookie': '__gads=ID=2e74240bce175f14:T=1633943015:S=ALNI_Mb4zNWh_Jw8g48mJBzAtI3GLfFowg; _ga=GA1.3.1120683331.1633943014; dable_uid=37221179.1605116191217; _fbp=fb.2.1633943020000.2017595486; _gid=GA1.3.762113030.1634093125',
			}
	try :
		response = requests.get(page1, proxies = proxy , headers=headers, timeout=50)
		print("succes : " + page1)
		break
	except requests.exceptions.RequestException as e:
		print("loop : " + page1)
		sleep(randint(1, 10))
		continue
status_code = response.status_code
page = 1
while status_code == 200 and page <= 15:
	link = str(url)+str(page)
	# print(link)
	user_agent = random.choice(user_agents)
	headers = {
			    'authority': 'www.orientaldaily.com.my',
			    'cache-control': 'max-age=0',
			    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
			    'sec-ch-ua-mobile': '?0',
			    'sec-ch-ua-platform': '"Windows"',
			    'upgrade-insecure-requests': '1',
			    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
			    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			    'sec-fetch-site': 'same-origin',
			    'sec-fetch-mode': 'navigate',
			    'sec-fetch-user': '?1',
			    'sec-fetch-dest': 'document',
			    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
			    'cookie': '__gads=ID=2e74240bce175f14:T=1633943015:S=ALNI_Mb4zNWh_Jw8g48mJBzAtI3GLfFowg; _ga=GA1.3.1120683331.1633943014; dable_uid=37221179.1605116191217; _fbp=fb.2.1633943020000.2017595486; _gid=GA1.3.762113030.1634093125',
			}
	sleep(randint(1,10))
	while True:
		try:
			response = requests.get(link, proxies=proxy, headers=headers, timeout=50)
			print("success :" + link)
			break
		except requests.exceptions.RequestException as e:
			print("loop : " + link)
			continue
	today = date.today()
	# print(response.status_code)

	#---------save index html------------#
	filename_index = "/home/amel/orientaldaily/html/index/{}/advertorial/index_{}.html".format(today,hash(link))
	os.makedirs(os.path.dirname(filename_index), exist_ok=True)
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
			print("title link :" + tl)
			user_agent = random.choice(user_agents)
			headers = {
					    'authority': 'www.orientaldaily.com.my',
					    'cache-control': 'max-age=0',
					    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
					    'sec-ch-ua-mobile': '?0',
					    'sec-ch-ua-platform': '"Windows"',
					    'upgrade-insecure-requests': '1',
					    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
					    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
					    'sec-fetch-site': 'same-origin',
					    'sec-fetch-mode': 'navigate',
					    'sec-fetch-user': '?1',
					    'sec-fetch-dest': 'document',
					    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
					    'cookie': '__gads=ID=2e74240bce175f14:T=1633943015:S=ALNI_Mb4zNWh_Jw8g48mJBzAtI3GLfFowg; _ga=GA1.3.1120683331.1633943014; dable_uid=37221179.1605116191217; _fbp=fb.2.1633943020000.2017595486; _gid=GA1.3.762113030.1634093125',
					}
			sleep(randint(5,10))
			while True:
				try:
					response_detail = requests.get(tl, proxies=proxy, headers=headers, timeout=50)
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
			list_url.append(tl)

		#---------save detail html------------#
			filename_content = "/home/amel/orientaldaily/html/content/{}/advertorial/detail_{}.html".format(today,hash(detail_url))
			os.makedirs(os.path.dirname(filename_content), exist_ok=True)
			with open(filename_content, 'w', encoding = 'utf-8') as f:
				f.write(str(response_detail.text))

	#-----------save detail json-------------#
			filename_json = "/home/amel/orientaldaily/json/content/{}/advertorial/detail_{}.json".format(today,hash(detail_url))
			os.makedirs(os.path.dirname(filename_json), exist_ok=True)
			with codecs.open(filename_json, 'w',encoding="utf-8") as f:
				f.write(str(json_data))
			data=data+1
			print("page : " + str(page))
			print("data : " + str(data))
		except Exception as e:
			print(e)
			print("skip : " + tl)
	page=page+1


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

message = "Engine : Oriental  \n" + "Category : Advertorial \n" + "Data : " + str(data)
telegram_bot_sendtext(str(message))
with codecs.open("/home/amel/orientaldaily/check_first_url_advertorial.json", 'w',encoding="utf_8_sig") as l:
  json.dump(list_url[0],l,ensure_ascii=False)
print("End")
