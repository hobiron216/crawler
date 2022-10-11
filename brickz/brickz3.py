import datetime
import requests
from bs4 import BeautifulSoup
import re
import json
import os
import time
from random import randint



class Brickz:
    def __init__(self):
        self.base_link = 'https://www.brickz.my/'
        self.PATH_SAVE = '/dataph/brickz'
        #self.PATH_SAVE = '/home/shahid/Documents/TugasmasEliaEM/brickz-code_201112/'
        self.a=0
        self.headers = {
            'authority': 'www.brickz.my',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.brickz.my/',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cookie': 'PHPSESSID=8r5acoas73uce6vd620bn02vm6; _ga=GA1.3.32078667.1639448619; _gid=GA1.3.1750479999.1639448619; _gat=1; fingerprint=61b8003674306; __atuvc=2%7C50; __atuvs=61b8002e1e5d810a001',
        }


        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
    def create_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path


    def get_page(self):
        while True :
            try:
                r= requests.get(self.base_link, headers=self.headers, timeout=50, proxies=self.proxies)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                print("loop : " + self.base_link)
                continue
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        categories = soup.select('#main_menu li a')
        for category in categories:
            link = category.get('href')
            category = category.text
            # print(category)
            while True :
                try:
                    r= requests.get(link, headers=self.headers, timeout=50, proxies=self.proxies)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    print("loop : " + link)
                    continue
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            next = soup.select('.pagination a')[-2].text.replace(',', '')
            for i in range(1, int(next)+1):
                try:
                  if category!="Industrial":
                      break
                  link_detail = "{}page/{}".format(link, i)
                  self.get_index(link_detail)
                except Exception as e:
                  print(e)
                  continue



    def get_index(self, link_detail):
        time.sleep(randint(3, 10))
        category_link = link_detail
        # category_link = "https://www.brickz.my/transactions/agriculture/page/7"
        category = re.sub('.*transactions\/(.*)\/page.*', '\g<1>', category_link)
        page = re.sub('.*page\/(.*)', '\g<1>', category_link)
        while True :
            try:
                r= requests.get(category_link, headers=self.headers, timeout=50, proxies=self.proxies)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                print("loop wkwk : " + category_link)

                continue
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select('#ptd_list_table')

        for row in table[0].findAll('tr'):
            col = row.findAll('td')
            if len(col) > 0:
                tmp = dict()
                link= col[0].find('a').get('href')
                link_date= link+"?range=2000+Jan-"
                tmp['link_detail'] = link_date
                tmp['title_detail'] = re.sub("\W", '_', str(col[0].find('a').text).strip())
                tmp['page'] = page
                print('get link details {}'.format(tmp['link_detail']))
                self.get_detail(data=tmp, category=category)

    def get_detail(self, data, category):
        try:
            w_date = datetime.datetime.now().strftime("%Y%m%d")
            link_detail = data['link_detail']
            title_detail = data['title_detail']
            page = data['page']
            #print("get transaction " + link_detail)
            while True :
                try:
                    r= requests.get(link_detail, headers=self.headers, timeout=50)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    continue

            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.select('#ptd_list_detail_table')
            status = True
            result_details = []
            while status:
                try :
                    time.sleep(randint(3, 9))
                    soup = BeautifulSoup(html, 'html.parser')
                    # print(soup)
                    # with open("tes.html",'w',encoding='utf8') as outfile:
                    #     outfile.write(str(soup))
                    table = soup.select('#ptd_list_detail_table')
                    headers = table[0].select('tr th a')
                    for row in table[0].findAll('tr'):

                        col = row.findAll('td')
                        if len(col) > 0:
                            tmp = dict()
                            for i in range(0, len(col) - 1):
                                tmp[str(headers[i].text).replace(' ', '_')] = col[i].text
                            result_details.append(tmp)
                            # print(result_details)
                    next = soup.select('.ptd_table_toolbar .pagination a')
                    if next:
                        if next[-1].text == "»":
                            link_next = next[-1].get('href')
                            print('NEXT {}'.format(link_next))
                            while True :
                                try:
                                    r= requests.get(link_next, headers=self.headers, timeout=50, proxies=self.proxies)
                                    html =r.text
                                    break
                                except requests.exceptions.RequestException as e:
                                    print(e)
                                    print("loop : " + link_next)
                                    continue
                            status = True
                        else:
                            status = False
                    else:
                        status = False
                except :
                    raise

            if result_details:
                result = dict()
                result['title'] = title_detail
                result['link_ori'] = link_detail
                result['Transactions'] = result_details

                if not os.path.isfile(
                        "{}/{}/{}/brickz_{}_page{}.json".format(self.PATH_SAVE, w_date, category, category, page)):
                    result_all = dict()
                    result_all.update({"data": [result]})
                    path = self.create_path("{}/{}/{}".format(self.PATH_SAVE, w_date, category))
                    with open("{}/brickz_{}_page{}.json".format(path, category, page), 'w') as f:
                        json.dump(result_all, f)
                    print("add new details {}".format(title_detail))
                else:
                    with open("{}/{}/{}/brickz_{}_page{}.json".format(self.PATH_SAVE, w_date, category, category, page),
                              'r') as f:
                        feed = json.load(f)
                    cek = []
                    for d in feed['data']:
                        cek.append(d['link_ori'])
                    if result['link_ori'] not in cek:
                        feed['data'].append(result)
                        with open("{}/{}/{}/brickz_{}_page{}.json".format(self.PATH_SAVE, w_date, category, category,
                                                                          page), 'w') as f:
                            json.dump(feed, f)
                        self.a = self.a +1
                        print('updated details {}'.format(title_detail))
                        print("Data : "+ str(self.a))
                        print("page : " + str(page))
                        print("category : " + category)
                    else:
                        print('exists link ori {}'.format(result['link_ori']))
                        print("Data : " + str(self.a))
                        print("page : " + str(page))
                        print("category : " + category)
        except Exception as e:
            print(e)
            raise

print(Brickz().get_page())

