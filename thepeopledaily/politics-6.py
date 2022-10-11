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
url = "http://politics.people.com.cn/GB/432731/index" #politics-6
page = 0
max_page = 6
# print(proxy_)

while page < max_page :
	proxy = {
		"http":"http://ProXy:Rahas!@2020@139.59.105.3:53128"
	}

	headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
		'Connection': 'keep-alive',
		'Host': 'politics.people.com.cn',
		'Referer': 'http://politics.people.com.cn/GB/432731/index.html',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
	# auth = HTTPProxyAuth("ProXy", "Rahas!@2020")
	page=page+1
	print("1st try")
	try :
		today = date.today()
		link = str(url)+str(page)+".html"
		print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
		print("Request Index Page "+str(page))
		sleep(randint(300,500))
		response = requests.get(link,proxies=proxy,headers=headers)
			# print(response.content)

				 #---------save index html------------#
		print("Saving HTML Index Page "+str(page))
		filename_index = "/home/amel/thepeopledaily/daily/html/index/{}/politics/politics-6/index_{}.html".format(today,hash(link))
		os.makedirs(os.path.dirname(filename_index), exist_ok=True)
		with codecs.open(filename_index, 'w', encoding = 'utf-8') as f:
			f.write(str(response.text))


			# 	#	---------parse html index from url title to req detail html-----------#
		soup = bs4.BeautifulSoup(response.content, 'html.parser')
		title_link = []
		for index in soup.select('.list_16.mt10>li>a'): #selector detail link in index page
		#.w1000.ej_content.mt30 > div> div> ul > li> a
			# print(index)
			link = index.get('href')
			# print(link)
			title_link.append(link)
		title_link_count = len(title_link)
		# print("Title Link : "+str(title_link))

		link_index_array = 0
		while link_index_array <= title_link_count :
			print("2nd try")
			try : 
				print("Link Index Array : "+str(link_index_array))
				# print(str(title_link[link_index_array]))
				detail_link = str(title_link[link_index_array]).replace("b'","").replace("'","")
				print("Detail Link 1 : "+str(detail_link))
				head_url = "http://politics.people.com.cn/"
				if "http://" not in str(detail_link) : 
					detail_link=head_url+str(title_link[link_index_array]).replace("b'","").replace("'","")
					print("Detail Link 2 : "+str(detail_link))			
				print("3rd try")
				try : 
					print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
					print("Request Detail Page "+str(page)+"_"+str(link_index_array))
					print(detail_link)
					sleep(randint(200,500))
					response_detail = requests.get(detail_link,proxies=proxy)
					# print(response_detail.content)

					# #	#---------parsing url, title, date, article to json--------#
					sp_detail = bs4.BeautifulSoup(response_detail.content,"lxml")
					# print(sp_detail)
					detail_title = sp_detail.title.text
					# print("Title : "+ str(detail_title))
					detail_url = detail_link #detail_link
					# print("URL : "+ str(detail_url))
					detail_date = sp_detail.find("meta", attrs={'name': 'publishdate'})['content'] #<meta name="publishdate" content="2020-06-30">
					# print("Date : "+str(detail_date))
					# detail_article = ""
					detail_article = sp_detail.select('.box_con>p')
					# print(len(detail_article)) #.content >p #picG >p
					# print(detail_article)
					if len(detail_article) == 0 :
						# print(len(detail_article))
						detail_article = sp_detail.select('.content.clear.clearfix>p')
						if len(detail_article) == 0 :
								detail_article = sp_detail.select('.rm_txt_con.cf>p')
						# print(detail_article)
					article = ""
					for tag in detail_article :
					# # 	# print(tag.text)
						if len(tag.text.strip()) != 0 :
							article = article+tag.text+"| "
					# print("Article : "+ str(article))
					json_data = {'title': str(detail_title), 'url': str(detail_url), 'date': str(detail_date),'article': str(article)}
					json_data = str(json_data).encode("utf_8_sig")
					json_data = json_data.decode('utf-8')
					# print(json_data)
					list_url.append(detail_link)

					# # #---------save detail html------------#
					print("Saving HTML Detail Page "+str(page)+"_"+str(link_index_array))
					filename_content = "/home/amel/thepeopledaily/daily/html/content/{}/politics/politics-6/detail_{}.html".format(today,hash(detail_url))
					os.makedirs(os.path.dirname(filename_content), exist_ok=True)
					with codecs.open(filename_content, 'w', encoding = 'utf-8') as f:
						f.write(str(response_detail.text))

					# # #-----------save detail json-------------#
					print("Saving JSON Detail Page "+str(page)+"_"+str(link_index_array))
					filename_json = "/home/amel/thepeopledaily/daily/json/content/{}/politics/politics-6/detail_{}.json".format(today,hash(detail_url))
					os.makedirs(os.path.dirname(filename_json), exist_ok=True)
					with codecs.open(filename_json, 'w') as f:
						f.write(str(json_data))
						data = data + 1

				except :
					print("ERROR PARSING DETAIL-SKIP")
					except_json = {'link':detail_link,'date':today,'category':'politics-6'}
					filename_except = "/home/amel/thepeopledaily/daily/except/content/{}/politics/politics-6/detail_except.json".format(today)
					os.makedirs(os.path.dirname(filename_except), exist_ok=True)
					with codecs.open(filename_except, 'a') as f:
						f.write(str(except_json)+"\n")

			except :
				print("ERROR COUNTER PAGE DETAIL")
			# 	pass
			link_index_array+=1
		print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
		print("Page "+str(page)+" done")
	except :
		print("ERROR INDEX")
		pass

print("END")
print(list_url[0])

message = "Engine : Thepeopledaily  \n" + "Category : politics-6 \n" +  "Data : " + str(data)
telegram_bot_sendtext(str(message))

with codecs.open("/home/amel/thepeopledaily/check_first_url_politics-6.json", 'w',encoding="utf_8_sig") as l:
  json.dump(list_url[0],l,ensure_ascii=False)