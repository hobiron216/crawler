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

list_url = []

data=0

url = "http://caijing.chinadaily.com.cn/5b7620c4a310030f813cf452/page_" #exclusive
page = 0
max_page = 10
# print(proxy_)

while page <= max_page :
	proxy = {
		"http":"http://139.59.105.3:53128"
	}
	proxy_2 = {
		"https":"https://139.59.105.3:53128"
		}
	auth = HTTPProxyAuth("ProXy", "Rahas!@2020")
	page=page+1
	# print("1st try")
	try :
		today = date.today()
		link = str(url)+str(page)+".html"
		print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
		print("Request Index Page "+str(page))
		response = requests.get(link, proxies=proxy, auth=auth)
	# 	print("page : "+str(page))

			# #---------save index html------------#
		filename_index = "/home/amel/chinadaily/daily/html/index/{}/exclusive/index_{}.html".format(today,hash(link))
		os.makedirs(os.path.dirname(filename_index), exist_ok=True)
		with open(filename_index, 'w', encoding = 'utf_8_sig') as f:
			f.write(str(response.text))

		#---------parse html index from url title to req detail html-----------#
		soup = bs4.BeautifulSoup(response.content, 'html.parser')
		title_link = []
		for index in soup.select('.busBox3>div>div>h3>a'):
			link = index.get('href')
			# print(link)
			title_link.append(link)
		# print(title_link)
		title_link_count = len(title_link)
		print("Length Title Link : " + str(title_link_count))

	#------looping title in index html to get detail html-------#

		link_index_array = 0
		while link_index_array < title_link_count :
			try :
				print("Link Index Array : "+str(link_index_array))
				# print(i)
				detail_link="http:"+str(title_link[link_index_array])
				try :
					sleep(randint(5,10))
					# print(title_link[i])
					# print(detail_link)
					print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
					print("Request Detail Page "+str(page)+"_"+str(link_index_array))
					response_detail = requests.get(detail_link,proxies=proxy_2, auth=auth)

				
		# 			 #---------parsing url, title, date, article to json--------#
					sp_detail = bs4.BeautifulSoup(response_detail.content,"html.parser")
					detail_title = sp_detail.title.text
		# 			# print("Title : "+ detail_title)
					detail_url = sp_detail.find("meta",  property="og:url")['content']
		# 			# print("URL : "+ detail_url)
					detail_date = sp_detail.find("meta", attrs={'name': 'publishdate'})['content']
		# 			# print("Date : " + detail_date)
					detail_article = sp_detail.select('#Content > p')
					article = ""
					for tag in detail_article :
		# 				# print(tag.text)
						if len(tag.text.strip()) != 0 :
							article = article+tag.text+"| "
		# 			# print("Article : "+ str(detail_article))
					json_data = {'title':detail_title, 'url':detail_url, 'date':detail_date,'article':article}
					list_url.append(detail_link)

			# # 	#---------save detail html------------#
					print("Saving HTML Detail Page "+str(page)+"_"+str(link_index_array))
					filename_content = "/home/amel/chinadaily/daily/html/content/{}/exclusive/detail_{}.html".format(today,hash(detail_url))
					os.makedirs(os.path.dirname(filename_content), exist_ok=True)
					with open(filename_content, 'w', encoding = 'utf_8_sig') as f:
						f.write(str(response_detail.text))

		# # #-----------save detail json-------------#
					print("Saving JSON Detail Page "+str(page)+"_"+str(link_index_array))
					filename_json = "/home/amel/chinadaily/daily/json/content/{}/exclusive/detail_{}.json".format(today,hash(detail_url))
					os.makedirs(os.path.dirname(filename_json), exist_ok=True)
					with codecs.open(filename_json, 'w',encoding="utf_8_sig") as f:
						f.write(str(json_data))
						data = data + 1
				except :
					print("ERROR PARSING DETAIL-SKIP")
					except_json = {'link':detail_link,'date':today,'category':'exclusive'}
					filename_except = "/home/amel/chinadaily/daily/except/content/{}/exclusive/detail_except.json".format(today)
					os.makedirs(os.path.dirname(filename_except), exist_ok=True)
					with codecs.open(filename_except, 'a',encoding="utf_8_sig") as f:
						f.write(str(except_json)+"\n")


			except :
				print("ERROR COUNTER PAGE DETAIL")
				pass
			link_index_array+=1
		print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
		print("Page "+str(page)+" done")
	except :
		print("ERROR INDEX")
		pass
print("End")
print(list_url[0])
message = "Engine : Chinadaily  \n" + "Category : cexclusive \n" +  "Data : " + str(data)
telegram_bot_sendtext(str(message))

with codecs.open("/home/amel/chinadaily/check_first_url_exclusive.json", 'w',encoding="utf_8_sig") as l:
  json.dump(list_url[0],l,ensure_ascii=False)