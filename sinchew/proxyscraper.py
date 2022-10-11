import json

from logger import Logger
from urllib.request  import urlopen
#from __init__ import CURRENT_DIR


logger = Logger('Proxyscraper')


class Proxyscrape:
    def __init__(self):
        self.url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all"
        self.raw_proxy_path = 'raw_proxy.txt'
        self.save_proxy_path = "proxy_https.json"

    def download(self):
        response = urlopen(self.url)
        data = response.read()
        txt_str = str(data)
        lines = txt_str.split("\\n")
        des_url = self.raw_proxy_path
        fx = open(des_url,"w")
        for line in lines:
            fx.write(line+ "\n")
        fx.close()

    def parse(self):
        result = []
        with open(self.raw_proxy_path, 'r') as reader:
            raw_proxy = reader.read()

        raw_proxy = raw_proxy.replace('\'', '')
        raw_proxy = raw_proxy.replace('b', '')
        raw_proxy = raw_proxy.replace('\\r', '')
        raw_proxy = raw_proxy.split('\n')

        for proxy in raw_proxy:
            temp = dict()
            try:
                address = proxy.split(':')[0]
                port = proxy.split(':')[1]
                temp['address'] = address
                temp['port'] = int(port)

                if temp['address'] != '' and temp['port'] != '':
                    result.append(temp)
            except:
                pass

        self.save_json(result)
        return result

    def save_json(self, data):
        with open(self.save_proxy_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    Proxyscrape().download()
    Proxyscrape().parse()
    logger.log('Process Completed!')
