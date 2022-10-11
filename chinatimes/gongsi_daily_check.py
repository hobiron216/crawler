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
import time
from requests.auth import HTTPProxyAuth
import sys
from datetime import datetime

def telegram_bot_sendtext(bot_message):
	global response
	bot_token = '1603186460:AAFaH_UjuERmIYthGcWWDeS80U7CRmWwpq4'
	bot_chatID = '-538195961'
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

	while True:
		try:
			response = requests.get(send_text, timeout=10)
			break
		except requests.exceptions.RequestException as e:
			print("gagal kirim telegram")
			continue

	return response.json()

with open("/home/amel/chinatimes/check_first_url_gongsi.json", 'r', encoding='utf_8_sig') as outfile:
  first_url= json.load(outfile)
list_url = []

data=0
# url = "https://www.chinatimes.net.cn/finance?werr=&page=" 
url ="https://www.chinatimes.net.cn/finance/gongsi?page=" #gongsi
page = 0
max_page = 5
# print(proxy_)

while page <= max_page :
	headers = {'Sec-Fetch-Dest': 'document',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-User': '?1',
	'Host': 'www.chinatimes.net.cn',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Referer': 'https://www.chinatimes.net.cn/finance?werr=',
	'Upgrade-Insecure-Requests': '1'}

	proxy = {
		"http":"https://ProXy:Rahas!@2020@139.59.105.3:53128"
	}
	page=page+1
	print("1st try")
	while True:
		try :
			today = date.today()
			hours = datetime.now().strftime("%H")
			link = str(url)+str(page)
			print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
			print("Request Index Page "+str(page))
			response = requests.get(link, proxies=proxy, headers=headers)
			print("page : "+str(page))

			#---------save index html------------#
			filename_index = "/home/amel/chinatimes/daily/html/index/{}/{}/gongsi/index_{}.html".format(today,hours,hash(link))
			os.makedirs(os.path.dirname(filename_index), exist_ok=True)
			with open(filename_index, 'w', encoding = 'utf_8_sig') as f:
				f.write(str(response.text))

			#---------parse html index from url title to req detail html-----------#
			soup = bs4.BeautifulSoup(response.content, 'html.parser')
			title_link = []
			for index in soup.select('.item>h2>a'): #selector detail link in index page
				link = index.get('href')
				# print(link)
				title_link.append(link)
			# print(title_link)
			title_link_count = len(title_link)
			print("Length Title Link : " + str(title_link_count))
			# print(title_link)

			#------looping title in index html to get detail html-------#

			link_index_array = 0
			while link_index_array < title_link_count :
				print("2nd try")
				# try :
				print("Link Index Array : "+str(link_index_array))
			# # 	# print(i)
				detail_link="https://www.chinatimes.net.cn"+str(title_link[link_index_array])
				# print(detail_link)
				print("url detail : "+detail_link)
				print("first url : "+first_url)
				if detail_link in first_url :
					message = "Engine : Chinatimes  \n" + "Category : gongsi-hourly \n" +  "Data : " + str(data)
					telegram_bot_sendtext(str(message))
					sys.exit("EXIT : url == first url")
				else :
					print("url != first url")
					print("3rd try")
				try :
					sleep(randint(5,10))
					# print(title_link[i])
					# print(detail_link)
					print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
					print("Request Detail Page "+str(page)+"_"+str(link_index_array))
					response_detail = requests.get(detail_link,proxies=proxy, headers=headers)

				
					# #	#---------parsing url, title, date, article to json--------#
					sp_detail = bs4.BeautifulSoup(response_detail.content,"html.parser")
					detail_title = sp_detail.title.text #.title>h1
					# print("Title : "+ detail_title)
					detail_url = detail_link #detail_link
					# print("URL : "+ detail_url)
					detail_date = sp_detail.select('.info>#pubtime_baidu') #.info>#pubtime_baidu
					detail_date = detail_date[0].text.split("：")
					detail_date = detail_date[1].split(" ")
					detail_date = detail_date[0]
					# print("Date : " + detail_date[0].text)
					detail_article = sp_detail.select('.infoMain>p') #.infoMain>p
					# print(detail_article)
					article = ""
					for tag in detail_article :
						# print(tag.text)
						if len(tag.text.strip()) != 0 :
							article = article+tag.text+"| "
					json_data = {'title':detail_title, 'url':detail_url, 'date':detail_date,'article':article}
					# print(json_data)
					list_url.append(detail_link)

					# # #---------save detail html------------#
					print("Saving HTML Detail Page "+str(page)+"_"+str(link_index_array))
					filename_content = "/home/amel/chinatimes/daily/html/content/{}/{}/gongsi/detail_{}.html".format(today,hours,hash(detail_url))
					os.makedirs(os.path.dirname(filename_content), exist_ok=True)
					with open(filename_content, 'w', encoding = 'utf_8_sig') as f:
						f.write(str(response_detail.text))

					# # #-----------save detail json-------------#
					print("Saving JSON Detail Page "+str(page)+"_"+str(link_index_array))
					filename_json = "/home/amel/chinatimes/daily/json/content/{}/{}/gongsi/detail_{}.json".format(today,hours,hash(detail_url))
					os.makedirs(os.path.dirname(filename_json), exist_ok=True)
					with codecs.open(filename_json, 'w',encoding="utf_8_sig") as f:
						f.write(str(json_data))
						data = data + 1

				except :
					print("ERROR PARSING DETAIL-SKIP")
					except_json = {'link':detail_link,'date':today,'category':'gongsi'}
					filename_except = "/home/amel/chinatimes/daily/except/content/{}/{}/gongsi/detail_except.json".format(today,hours)
					os.makedirs(os.path.dirname(filename_except), exist_ok=True)
					with codecs.open(filename_except, 'a',encoding="utf_8_sig") as f:
						f.write(str(except_json)+"\n")

				# except :
				# 	print("ERROR COUNTER PAGE DETAIL")
				# 	pass
				link_index_array+=1
			print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
			print("Page "+str(page)+" done")
			break
		except Exception as e:
			print("ERROR INDEX")
			print(e)
			
message = "Engine : Chinatimes  \n" + "Category : gongsi-hourly \n" +  "Data : " + str(data)
telegram_bot_sendtext(str(message))

with codecs.open("/home/amel/chinatimes/check_first_url_gongsi.json", 'w',encoding="utf_8_sig") as l:
  json.dump(list_url[0],l,ensure_ascii=False)