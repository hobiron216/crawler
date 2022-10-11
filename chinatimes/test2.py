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
import requests.auth

url = "https://www.chinatimes.net.cn/finance?werr=&page=" #/gongyicaijing
page = 1
max_page = 2
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
		"https":"https://ProXy:Rahas!@2020@139.59.105.3:53128"
	}
	page=page+1
	# print("1st try")
	# try :
	today = date.today()
	link = str(url)+str(page)
	print(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))
	print("Request Index Page "+str(page))
	response = requests.get(link, proxies=proxy, headers=headers)
	print(response.content)


		#---------parse html index from url title to req detail html-----------#
	# soup = bs4.BeautifulSoup(response.content, 'html.parser')
	# title_link = []
	# for index in soup.select('.item>h2>a'): #selector detail link in index page
	# 	link = index.get('href')
	# 	# print(link)
	# 	title_link.append(link)
	# # print(title_link)
	# title_link_count = len(title_link)
	# print("Length Title Link : " + str(title_link_count))