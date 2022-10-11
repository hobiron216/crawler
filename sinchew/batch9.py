import hashlib
import time

import requests
from pathlib import Path
import datefinder
from pyvirtualdisplay import Display
from selenium import webdriver

from logger import Logger
from datetime import  date
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from requests.exceptions import Timeout
class Sinchew:


    def create_folder(self,crawl_date):
        # Path("/home/shahid/Documents/requests/news/sinchew/html/"+ crawl_date+ "/world/").mkdir(parents=True, exist_ok=True)
        # Path("/home/shahid/Documents/requests/news/sinchew/json/" + crawl_date + "/world/").mkdir(parents=True, exist_ok=True)
        Path("/home/shahid/Documents/TugasmasEliaEM/cina2/dataph/requests/news/sinchew/batch2/html/"+crawl_date+ "/category/" ).mkdir(parents=True, exist_ok=True)
        Path("/home/shahid/Documents/TugasmasEliaEM/cina2/dataph/requests/news/sinchew/batch2/json/"+crawl_date+ "/category/" ).mkdir(parents=True, exist_ok=True)
        # "/dataph/requests/news/sinchew/html/" + crawl_date + "/world/" + href21 + ".html"

    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)
        self.base_link = "https://www.sinchew.com.my/"
        self.a = 0
        #self.display = Display(visible=0, size=(1366, 768))
        #self.display.start()


    def get_items(self):
        #self.browser = self.get_browser()
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        self.create_folder(crawl_date)
        i=9629
        while i<100000:
            i=i+1
            self.get_parser(crawl_date, self.a,i)#,self.browser)
            print(i)

    def get_browser(self):
        browser = webdriver.Firefox()#executable_path='/usr/local/bin/geckodriver')
        browser.maximize_window()
        return browser
    def get_parser(self, crawl_date,a,i):#,browser):
            url = self.base_link + "content/content_"+ str(i) + ".html"
            #headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

            valid=False
            while not valid:
            	try:
            		r = requests.get(url)
            		#browser.get(url)
            		valid=True

            	except TimeoutException:
            		continue


            #html = browser.page_source
            html = r.text
            v= True
            while v :
                soup=BeautifulSoup(html,"html.parser")
                time21=soup.find("div", attrs={"style":"width:670px;text-align:left;float:left;margin-top:10px;border-right: 1px solid #ccc;"})
                if time21==None:
                    print("awwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
                    v=False
                    break
                else :
                    time21=time21.get_text().split(" ")
                match = datefinder.find_dates(time21[0])
                e=0
                for ndate in match:
                    e=e+1
                    if e>3:
                        break
                    title=soup.find("h1", attrs={"style":"color:black;font-size:34px;"})
                    if title==None:
                        title= soup.find("div", attrs={"style":"color:black;font-size:34px;"}).get_text()
                    else :
                        title= title.get_text()
                    # headlines= soup.find("div", attrs={"style":"color:#cd2026;font-size:16px"}).get_text()
                    category=soup.find("div", class_="neiwen-top-title").get_text().replace("\n","")
                    article=soup.find("div", id="dirnum").get_text()

                    href21= hashlib.md5(url.encode('utf-8')).hexdigest().upper()
                    path_html = "/dataph/requests/news/sinchew/batch/html/"+crawl_date+ "/category/" + href21 + ".html"



                    ndate=ndate.strftime("%Y-%m-%d %H:%M:%S")


                    result = {

                                    "title": title,
                                    "article": article,
                                    "ndate": ndate,
                                    "category": category,
                                    "crawl_date" : crawl_date,
                                    "path_html" : path_html,
                                    "url"       : url


                                }
                    self.a = self.a + 1

                    #print(result)
                    print("jumlah data : " + str(self.a))
                    print("url : " + url)
                    v = False

                # print(obj)/home/shahid/Documents/TugasmasEliaEM/cina2/dataph

                    with open("/home/shahid/Documents/TugasmasEliaEM/cina2/dataph/requests/news/sinchew/batch2/html/"+crawl_date+ "/category/" + href21 + ".html", 'w') as outfile:
                        outfile.write(str(soup))
                    with open("/home/shahid/Documents/TugasmasEliaEM/cina2/dataph/requests/news/sinchew/batch2/json/"+crawl_date+ "/category/" + href21 + ".json", 'w') as outfile:
                        outfile.write(str(result))
                v = False
                # with open('cina.json', 'w') as outfile:
                #     outfile.write(str(result))
            return self.a

    def quit_browser(self):
        try:
            if self.browser:
                self.browser.quit()
                self.display.stop()
                self.logger.log('quit browser ...')
        except:
            raise

print(Sinchew().get_items())
