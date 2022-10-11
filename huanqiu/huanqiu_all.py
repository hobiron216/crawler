import hashlib
import json
import random
import socket
import time
import urllib

import requests
from pathlib import Path
import datefinder
from pyvirtualdisplay import Display
from selenium import webdriver

from logger import Logger
from datetime import date
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from requests.exceptions import Timeout
from urllib.request import urlopen
from selenium.webdriver import DesiredCapabilities, FirefoxProfile
from selenium.webdriver.firefox.options import Options
import ast
import random


class Huanqiu:

    def create_folder(self, crawl_date, category):
        # Path("/home/shahid/Documents/requests/news/sinchew/html/"+ crawl_date+ "/world/").mkdir(parents=True, exist_ok=True)
        # Path("/home/shahid/Documents/requests/news/sinchew/json/" + crawl_date + "/world/").mkdir(parents=True, exist_ok=True)
        Path("/dataph/requests/news/huanqiu/batch/html/" + crawl_date + "/" + category + "/").mkdir(parents=True,
                                                                                                    exist_ok=True)
        Path("/dataph/requests/news/huanqiu/batch/json/" + crawl_date + "/" + category + "/").mkdir(parents=True,
                                                                                                    exist_ok=True)
        # "/dataph/requests/news/sinchew/html/" + crawl_date + "/world/" + href21 + ".html"

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        # self.base_link = "https://china.huanqiu.com/"
        self.a = -1
        self.display = Display(visible=0, size=(1366, 768))
        self.display.start()
        # self.url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all"
        self.url = "https://api.getproxylist.com/proxy?apiKey=62e9cf6f693a1701c2ba9497f712fb048064bc46&allowsHttps=true&minDownloadSpeed=100&protocol=http"
        self.raw_proxy_path = 'raw_proxy.txt'
        self.save_proxy_path = "proxy_https.json"

    # def download(self):
    #     response = urlopen(self.url)
    #     data = response.read()
    #     txt_str = str(data)
    #     lines = txt_str.split("\\n")
    #     des_url = self.raw_proxy_path
    #     fx = open(des_url,"w")
    #     for line in lines:
    #         fx.write(line+ "\n")
    #     fx.close()

    # def parse(self):
    #     result = []
    #     with open(self.raw_proxy_path, 'r') as reader:
    #         raw_proxy = reader.read()

    #     raw_proxy = raw_proxy.replace('\'', '')
    #     raw_proxy = raw_proxy.replace('b', '')
    #     raw_proxy = raw_proxy.replace('\\r', '')
    #     raw_proxy = raw_proxy.split('\n')

    #     for proxy in raw_proxy:
    #         temp = dict()
    #         try:
    #             address = proxy.split(':')[0]
    #             port = proxy.split(':')[1]
    #             temp['address'] = address
    #             temp['port'] = int(port)

    #             if temp['address'] != '' and temp['port'] != '':
    #                 result.append(temp)
    #         except:
    #             pass

    #     self.save_json(result)
    #     return result

    # def save_json(self, data):
    #     with open(self.save_proxy_path, 'w') as f:
    #         json.dump(data, f, ensure_ascii=False, indent=4)

    # def proxy(self):
    #     address = None
    #     port = None
    #     try:
    #         with open('proxy_https.json', 'r') as f:
    #             proxies = f.read()
    #             proxies = json.loads(proxies)
    #             f.close()

    #         random.shuffle(proxies)
    #         rand_proxy = random.choice(proxies)
    #         self.address = rand_proxy['address']
    #         self.port = rand_proxy['port']

    #         socket.setdefaulttimeout(120)
    #         proxyList = [str(self.address)+":"+str(self.port)]

    #         for currentProxy in proxyList:
    #             if self.is_bad_proxy(currentProxy):
    #                 print("Bad Proxy %s" % (currentProxy))
    #             else:
    #                 print("%s is working" % (currentProxy))
    #                 q=False
    #     except Exception as e:
    #         self.logger.log(e, level='error')

    #     if self.address and self.port:
    #         proxy = {
    #             'http': '{}:{}'.format(self.address, self.port),
    #             'https': '{}:{}'.format(self.address, self.port),
    #             'ssl': '{}:{}'.format(self.address, self.port),
    #             'socks': '{}:{}'.format(self.address, self.port),
    #             'ftp': '{}:{}'.format(self.address, self.port)
    #         }
    #     self.logger.log('trying with proxy {}:{}'.format(self.address, self.port))

    #     return proxy

    def proxy(self):
        self.address = None
        self.port = None
        try:
            z=True
            while z:
                try:
                    r = requests.get(self.url,timeout=50)
                    z=False
                except requests.exceptions.RequestException as e:
                    continue
            r = r.text
            r = json.loads(r)

            # r=BeautifulSoup(r,"html.parser")
            self.address = r['ip']
            self.port = r['port']

            socket.setdefaulttimeout(120)
            proxyList = [str(self.address) + ":" + str(self.port)]

            for currentProxy in proxyList:
                if self.is_bad_proxy(currentProxy):
                    print("Bad Proxy %s" % (currentProxy))
                else:
                    print("%s is working" % (currentProxy))
                    q = False
        except Exception as e:
            self.logger.log(e, level='error')

        if self.address and self.port:
            proxy = {
                'http': '{}:{}'.format(self.address, self.port),
                'https': '{}:{}'.format(self.address, self.port),
                'ssl': '{}:{}'.format(self.address, self.port),
                'socks': '{}:{}'.format(self.address, self.port),
                'ftp': '{}:{}'.format(self.address, self.port)
            }
        self.logger.log('trying with proxy {}:{}'.format(self.address, self.port))

        return proxy

    def is_bad_proxy(self, pip):
        try:
            proxy_handler = urllib.request.ProxyHandler({'http': pip})
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            req = urllib.request.Request('https://world.huanqiu.com/article/40J2kxOZD6V')  # change the URL to test here
            sock = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print('Error code: ', e.code)
            return e.code
        except Exception as detail:
            print("ERROR:", detail)
            return True
        return False

    def get_items(self, proxy):
        # self.browser = self.get_browser()
        
        categorys = ['world', 'china', 'mil', 'taiwan', 'opinion', 'finance', 'tech']
        list_link = []
        for category in categorys:
            a = True
            i = 0
            while a:
                today = date.today()
                crawl_date = today.strftime("%Y%m%d")
                self.create_folder(crawl_date, category)
                i = i + 20
                url = "https://" + category + ".huanqiu.com/"
                url_api = "https://" + category + ".huanqiu.com/api/list?node=%22/e3pmh22ph/e3pmh2398%22,%22/e3pmh22ph/e3pmh26vv%22,%22/e3pmh22ph/e3pn6efsl%22,%22/e3pmh22ph/efp8fqe21%22&offset=" + str(
                    i) + "&limit=20"
                if i > 9980:
                    a = False
                    continue
                c = True
                x = 0
                while c:
                    try:
                        x = x + 1
                        if x >= 5:
                            proxy = self.proxy()
                        api = requests.get(url_api, proxies=proxy, timeout=50)
                        c = False
                    except requests.exceptions.RequestException as e:
                        print("connect api timeout")
                        # proxy=Huanqiu().proxy()
                        continue
                api = api.text
                api = json.loads(api)
                aw = api['list'][0]['aid']

                for j in range(0, 20):
                    link = api['list'][j]['aid']
                    list_link.append(link)
                # print(list_link)
                self.parser(url, list_link, proxy, crawl_date, category, i)
                del list_link[:]

    def parser(self, url, list_link, proxy, crawl_date, category, i):
        for k in list_link:
            self.a = self.a + 1
            # if category =='world' and self.a==0:
            # continue
            url21 = url + "article/" + str(k)
            # print(url21)
            b = True
            x = 0
            while b:
                try:
                    x = x + 1
                    if x >= 5:
                        proxy = self.proxy()
                    r = requests.get(url21, proxies=proxy, timeout=50)
                    b = False
                except requests.exceptions.RequestException as e:
                    print("connetion timeout")
                    # proxy=Huanqiu().proxy()
                    continue

            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find("div", class_="t-container-title").get_text()
            article = soup.find("div", class_="l-con clear").get_text()
            ndate = soup.find("p", class_="time").get_text()

            href21 = hashlib.md5(url21.encode('utf-8')).hexdigest().upper()
            path_html = "/dataph/requests/news/huanqiu/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html"

            result = {

                "title": title,
                "article": article,
                "ndate": ndate,
                "category": category,
                "crawl_date": crawl_date,
                "path_html": path_html,
                "url": url21

            }
            # print (result)
            with open("/dataph/requests/news/huanqiu/batch/html/" + crawl_date + "/" + category + "/" + href21 + ".html",
                      'w',encoding='utf8') as outfile:
                outfile.write(str(soup))
            with open("/dataph/requests/news/huanqiu/batch/json/" + crawl_date + "/" + category + "/" + href21 + ".json",
                      'w',encoding='utf8') as outfile:
                outfile.write(str(result))
            print("jumlah data: " + str(self.a))
            print("category : " + category)
            print("page : " + str(i))


# Huanqiu().download()
# Huanqiu().parse()
a = True
proxy = Huanqiu().proxy()
while a:
    try:
        r = requests.get("https://energy.huanqiu.com/article/40JD8biMgkP", proxies=proxy, timeout=50)
        a = False
    except requests.exceptions.RequestException as e:
        print("connetion timeout")
        proxy = Huanqiu().proxy()
        continue
proxy = Huanqiu().proxy()
print(Huanqiu().get_items(proxy))

