import hashlib
import json
import requests
from pathlib import Path

from datetime import date
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
import random
import time
from dateutil.parser import parse
import json
class run:

    def create_folder(self, category, crawl_date):
        Path(self.path + crawl_date + "/" + category + "/").mkdir(parents=True,exist_ok=True)

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def __init__(self):
        self.base_link = "https://www.traveloka.com/en-my/hotel/malaysia"
        self.a = 0
        self.proxies = { 'http' : 'http://ProXy:Rahas!@2020@139.59.105.3:53128'}
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        self.path = "/home/traveloka_hotel/"

    def get_items(self):
        categorys= ['penang', 'kuala-lumpur', 'terengganu', 'johor', 'kelantan', 'perlis', 'sabah', 'selangor', 'pahang',
                    'perak', 'kedah', 'sarawak', 'negeri sembilan' 'melaka', 'federal-teritory-of-labuan']
        for category in categorys:
            if category == 'penang':
                geoid = "107984"
                self.get_json(category, geoid)
            elif category == 'kuala-lumpur':
                geoid = "30012270"
                self.get_json(category, geoid)
            elif category == 'terengganu':
                geoid = "107982"
                self.get_json(category, geoid)
            elif category == 'johor':
                geoid = "10011654"
                self.get_json(category, geoid)
            elif category == 'kelantan':
                geoid = "10011656"
                self.get_json(category, geoid)
            elif category == 'perlis':
                geoid = "108033"
                self.get_json(category, geoid)
            elif category == 'selangor':
                geoid = "10011659"
                self.get_json(category, geoid)
            elif category == 'pahang':
                geoid = "10011657"
                self.get_json(category, geoid)
            elif category == 'perak':
                geoid = "10011658"
                self.get_json(category, geoid)
            elif category == 'kedah':
                geoid = "10011655"
                self.get_json(category, geoid)
            elif category == 'sarawak':
                geoid = "10011660"
                self.get_json(category, geoid)
            elif category == 'negeri sembilan':
                geoid = "10011661"
                self.get_json(category, geoid)
            elif category == 'melaka':
                geoid = "107980"
                self.get_json(category, geoid)
            elif category == 'federal-teritory-of-labuan':
                geoid = "107977"
                self.get_json(category, geoid)

    def page(self, geoid):
        user_agent = random.choice(self.user_agents)
        headers = {
            'authority': 'www.traveloka.com',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'x-route-prefix': 'en-my',
            'user-agent': user_agent,
            'x-domain': 'accomSearch',
            'content-type': 'application/json',
            'accept': 'application/json',
            'x-nonce': 'ecfc8274-abef-4ae8-8ec0-1837e47703b9',
            'origin': 'https://www.traveloka.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.traveloka.com/en-my/hotel/search?spec=01-04-2021.02-04-2021.1.1.HOTEL_GEO.107979.Kuala%20Lumpur.1',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'cookie': 'G_ENABLED_IDPS=google; datadome=QuyVTLKJ6M-h-LDmJepDdOAjEX.6V~fhyMc-e5gqRLLUA2BG8ZuQnd~2oip83UOGZ0Uvp_w7Nc7Bdr49pmabvIE~mhZjbH2rDGymmXMb3s; bm_sz=4932E225A1A12937BC59FDB9BF8973A4~YAAQfEZYaE/PIHR4AQAAd7LbhgtuJCkmkG25ywl9C4s/o21kuQxdefycpEgSbbBnlJkwAh1GrAT+ebos2TODt7vQNX1cRy15E3Hz5y+B+QETw/H5HdtytYJpmoYKt9WssM/ToRyzW/lUWYIr58Eie24UFFL64QYpvp+RBykB4mcoaEv0IUaSiMXu7rWzksC2u6uh; tv-repeat-visit=true; accomHomepagePopup=1; ak_bmsc=D7D346DE44024256596D75CA9BE625C36858467CC3650000480F64604FFA3D7E~plAlDs0LESCedAFXid6WNYdrngzCb8loRCH5155DyxOa7Q0jJxcmqELmPqKwtHb9t5OF3vSZWpkav+GWTmiWNqz8+UxjPypnpaADyx1ZEyylZb9Gji3cERxAXZUClqVzW3j0BFmFWPxW7lQrQ5IvDax0QMg64c5lsCl2OaoKEFV+y0FpOHjSadZSg9PRa84Y/JiOoQSNBNVWnpfH3rlCH5jUc6WgBn7NzDSdvTO1nCdPgEaDLQfZ5RPAeh4/wbEZXC; _fbp=fb.1.1617170251242.657880147; _gcl_au=1.1.989647063.1617170251; _gid=GA1.2.417891485.1617170251; _abck=D155552B879D9FEB7F0894D1800F1EBF~0~YAAQfEZYaF7PIHR4AQAAJMHbhgXLnzk2wUiCvhZK7u3Kehxp7SmCbKdVflXFB9yrVlAXfA+DlXylhLuetnL9849QezLydHeHNGyy0dHG/K3dvDa/eYT1n/rRCg3Xe0R7CN0iWcXioMRxz3s4EgH3WP0/WcsOF6YoCSLCzrvIo4ZJejgTcvlGzvwyxZ4Jg0PuYT9TAAMWcQsXFZU1UR49DInrJZODSz9Or/7UpX8pW/qdZD5j3Ps06bzg7C5NY5yQH3SETF1lYyF9jF+sGM+EJvmmprCygq0NT8SZE3ZzF5nsUEOvRGDM7nQdkFGAIpbr+U0aUluR1hg9pVBh+1nr/CBXaStW6F12VWzm523JO1HL/89VGio3QbG7MZTKfZ1UcUwIYwwzgkY9z52ldXd+vcDf1Iv9UAKJvXFg~-1~||-1||~-1; tv-fingerprint=UNKNOWN; tvs=qgdHX7GvehrD9XH5a3S4PWL3Nd74xArIuT+JzcRMbKddQHovERAJ9HWRLrAaZ0jPhWj5HSxm0ZKiRbldET1ham2PeYg1sQr2h/wIBjIyPQ1JQfOnq9PrXiJXCb7pG+GuO9j/UmBfY5mgg8Swk3uMVfkT0joTjoIvrHag4mvsav9m8f/kUv0Gn+d1oETlCR3R3jW7f6f85zK7XA1xLrLbn3wpMY91AYFzJ6h8za/vSrng40uUoDT+qJIv0oQGNB1A; accomSuccessLoginConfirmation=0; isPriceFinderActive=null; dateIndicator=null; bannerMessage=null; displayPrice=null; _gat_UA-29776811-12=1; _ga=GA1.2.2099670014.1607581180; tvl=qgdHX7GvehrD9XH5a3S4PdE8AYpuF3hYPaT5bxhY7ZbjrkUZUd0taNYVGz6HDbyQmsH1M/L+TqPKKj+uQWBgNK7djdtZRAayS1RiBLPeIvS5ToLEvGBDfrSDsJ7hWFUEqw0IdvVwN5TRKL7GhWYH8S/l9wfmgZudQVEgUGCLaR3vlyHfFnPptZUxAgMVwRNSCMYWUJplNNMY2P4/83O9X+8GNrPf8Ng75ZieUaJama8=; bm_sv=1D8823130430965B546A4E0433819A9F~MbXWQcDAheE3gAYFo7fCbqQfI0ySnaKOJ1mgqGYZQueUrNRqkXIa8gf5hG0q1BJbxKG6yTJbk8Digm1/dpMY0bnOZUefpFAnlS4RXx4/nIrjNZYErS4KmwYvhdtbc+wh7rsxFfRBO3yadCIqBmKp9HkpuX12E4rH3e/G0tD0O9M=; amp_1a5adb=5Ih7Ft7iw_2TQOIB060_M2...1f23dnfah.1f23hbh8a.c.0.c; _ga_RSRSMMBH0X=GS1.1.1617170251.4.1.1617174060.0',
        }

        data = '{"clientInterface":"desktop","data":{"checkInDate":{"year":2021,"month":4,"day":1},"checkOutDate":{"year":2021,"month":4,"day":2},"numOfNights":1,"currency":"MYR","numAdults":1,"numChildren":0,"childAges":[],"numInfants":0,"numRooms":1,"ccGuaranteeOptions":{"ccInfoPreferences":["CC_TOKEN","CC_FULL_INFO"],"ccGuaranteeRequirementOptions":["CC_GUARANTEE"]},"rateTypes":["PAY_NOW","PAY_AT_PROPERTY"],"isJustLogin":false,"backdate":false,"geoId":"%s","geoLocation":null,"monitoringSpec":{"lastKeyword":"Kuala Lumpur","searchId":null,"searchFunnelType":null,"isPriceFinderActive":"null","dateIndicator":"null","bannerMessage":"null","displayPrice":null},"showHidden":false,"locationName":"Kuala Lumpur, Malaysia","sourceType":"HOTEL_GEO","boundaries":null,"contexts":{"isFamilyCheckbox":false},"basicFilterSortSpec":{"accommodationTypeFilter":[],"ascending":false,"basicSortType":"POPULARITY","facilityFilter":[],"maxPriceFilter":null,"minPriceFilter":null,"quickFilterId":null,"starRatingFilter":[true,true,true,true,true],"top":100,"hasFreeCancellationRooms":false},"criteriaFilterSortSpec":null,"isExtraBedIncluded":true,"isUseHotelSearchListAPI":true,"supportedDisplayTypes":["INVENTORY","INVENTORY_LIST","HEADER","INVENTORY_WITH_HEADER"],"userSearchPreferences":[],"uniqueSearchId":"1695729899072935922"},"fields":[]}'%geoid

        response = requests.post('https://www.traveloka.com/api/v2/hotel/searchList', headers=headers, data=data)
        json_data=response.text


        json_data=json.loads(json_data)
        total= json_data['data']['numOfHotels']
        return total

    def get_json(self, category, geoid):
        total= self.page(geoid)
        i=0
        skip=0
        while True:
            i=i+1
            if skip > int(total):
                break


            user_agent = random.choice(self.user_agents)
            headers = {
                'authority': 'www.traveloka.com',
                'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'x-route-prefix': 'en-my',
                'user-agent': user_agent,
                'x-domain': 'accomSearch',
                'content-type': 'application/json',
                'accept': 'application/json',
                'x-nonce': 'ecfc8274-abef-4ae8-8ec0-1837e47703b9',
                'origin': 'https://www.traveloka.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.traveloka.com/en-my/hotel/search?spec=01-04-2021.02-04-2021.1.1.HOTEL_GEO.107979.Kuala%20Lumpur.1',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': 'G_ENABLED_IDPS=google; datadome=QuyVTLKJ6M-h-LDmJepDdOAjEX.6V~fhyMc-e5gqRLLUA2BG8ZuQnd~2oip83UOGZ0Uvp_w7Nc7Bdr49pmabvIE~mhZjbH2rDGymmXMb3s; bm_sz=4932E225A1A12937BC59FDB9BF8973A4~YAAQfEZYaE/PIHR4AQAAd7LbhgtuJCkmkG25ywl9C4s/o21kuQxdefycpEgSbbBnlJkwAh1GrAT+ebos2TODt7vQNX1cRy15E3Hz5y+B+QETw/H5HdtytYJpmoYKt9WssM/ToRyzW/lUWYIr58Eie24UFFL64QYpvp+RBykB4mcoaEv0IUaSiMXu7rWzksC2u6uh; tv-repeat-visit=true; accomHomepagePopup=1; ak_bmsc=D7D346DE44024256596D75CA9BE625C36858467CC3650000480F64604FFA3D7E~plAlDs0LESCedAFXid6WNYdrngzCb8loRCH5155DyxOa7Q0jJxcmqELmPqKwtHb9t5OF3vSZWpkav+GWTmiWNqz8+UxjPypnpaADyx1ZEyylZb9Gji3cERxAXZUClqVzW3j0BFmFWPxW7lQrQ5IvDax0QMg64c5lsCl2OaoKEFV+y0FpOHjSadZSg9PRa84Y/JiOoQSNBNVWnpfH3rlCH5jUc6WgBn7NzDSdvTO1nCdPgEaDLQfZ5RPAeh4/wbEZXC; _fbp=fb.1.1617170251242.657880147; _gcl_au=1.1.989647063.1617170251; _gid=GA1.2.417891485.1617170251; _abck=D155552B879D9FEB7F0894D1800F1EBF~0~YAAQfEZYaF7PIHR4AQAAJMHbhgXLnzk2wUiCvhZK7u3Kehxp7SmCbKdVflXFB9yrVlAXfA+DlXylhLuetnL9849QezLydHeHNGyy0dHG/K3dvDa/eYT1n/rRCg3Xe0R7CN0iWcXioMRxz3s4EgH3WP0/WcsOF6YoCSLCzrvIo4ZJejgTcvlGzvwyxZ4Jg0PuYT9TAAMWcQsXFZU1UR49DInrJZODSz9Or/7UpX8pW/qdZD5j3Ps06bzg7C5NY5yQH3SETF1lYyF9jF+sGM+EJvmmprCygq0NT8SZE3ZzF5nsUEOvRGDM7nQdkFGAIpbr+U0aUluR1hg9pVBh+1nr/CBXaStW6F12VWzm523JO1HL/89VGio3QbG7MZTKfZ1UcUwIYwwzgkY9z52ldXd+vcDf1Iv9UAKJvXFg~-1~||-1||~-1; tv-fingerprint=UNKNOWN; tvs=qgdHX7GvehrD9XH5a3S4PWL3Nd74xArIuT+JzcRMbKddQHovERAJ9HWRLrAaZ0jPhWj5HSxm0ZKiRbldET1ham2PeYg1sQr2h/wIBjIyPQ1JQfOnq9PrXiJXCb7pG+GuO9j/UmBfY5mgg8Swk3uMVfkT0joTjoIvrHag4mvsav9m8f/kUv0Gn+d1oETlCR3R3jW7f6f85zK7XA1xLrLbn3wpMY91AYFzJ6h8za/vSrng40uUoDT+qJIv0oQGNB1A; accomSuccessLoginConfirmation=0; isPriceFinderActive=null; dateIndicator=null; bannerMessage=null; displayPrice=null; _gat_UA-29776811-12=1; _ga=GA1.2.2099670014.1607581180; tvl=qgdHX7GvehrD9XH5a3S4PdE8AYpuF3hYPaT5bxhY7ZbjrkUZUd0taNYVGz6HDbyQmsH1M/L+TqPKKj+uQWBgNK7djdtZRAayS1RiBLPeIvS5ToLEvGBDfrSDsJ7hWFUEqw0IdvVwN5TRKL7GhWYH8S/l9wfmgZudQVEgUGCLaR3vlyHfFnPptZUxAgMVwRNSCMYWUJplNNMY2P4/83O9X+8GNrPf8Ng75ZieUaJama8=; bm_sv=1D8823130430965B546A4E0433819A9F~MbXWQcDAheE3gAYFo7fCbqQfI0ySnaKOJ1mgqGYZQueUrNRqkXIa8gf5hG0q1BJbxKG6yTJbk8Digm1/dpMY0bnOZUefpFAnlS4RXx4/nIrjNZYErS4KmwYvhdtbc+wh7rsxFfRBO3yadCIqBmKp9HkpuX12E4rH3e/G0tD0O9M=; amp_1a5adb=5Ih7Ft7iw_2TQOIB060_M2...1f23dnfah.1f23hbh8a.c.0.c; _ga_RSRSMMBH0X=GS1.1.1617170251.4.1.1617174060.0',
            }

            data = '{"clientInterface":"desktop","data":{"checkInDate":{"year":2021,"month":4,"day":1},"checkOutDate":{"year":2021,"month":4,"day":2},"numOfNights":1,"currency":"MYR","numAdults":1,"numChildren":0,"childAges":[],"numInfants":0,"numRooms":1,"ccGuaranteeOptions":{"ccInfoPreferences":["CC_TOKEN","CC_FULL_INFO"],"ccGuaranteeRequirementOptions":["CC_GUARANTEE"]},"rateTypes":["PAY_NOW","PAY_AT_PROPERTY"],"isJustLogin":false,"backdate":false,"geoId":"%s","geoLocation":null,"monitoringSpec":{"lastKeyword":"Kuala Lumpur","searchId":null,"searchFunnelType":null,"isPriceFinderActive":"null","dateIndicator":"null","bannerMessage":"null","displayPrice":null},"showHidden":false,"locationName":"Kuala Lumpur, Malaysia","sourceType":"HOTEL_GEO","boundaries":null,"contexts":{"isFamilyCheckbox":false},"basicFilterSortSpec":{"accommodationTypeFilter":[],"ascending":false,"basicSortType":"POPULARITY","facilityFilter":[],"maxPriceFilter":null,"minPriceFilter":null,"quickFilterId":null,"starRatingFilter":[true,true,true,true,true],"top":100,"hasFreeCancellationRooms":false,"skip":%s},"criteriaFilterSortSpec":null,"isExtraBedIncluded":true,"isUseHotelSearchListAPI":true,"supportedDisplayTypes":["INVENTORY","INVENTORY_LIST","HEADER","INVENTORY_WITH_HEADER"],"userSearchPreferences":[],"uniqueSearchId":"1695729899072935922"},"fields":[]}'%(geoid ,skip)

            response = requests.post('https://www.traveloka.com/api/v2/hotel/searchList', headers=headers, data=data)
            crawl_date=self.crawl_date()
            self.create_folder(category, crawl_date)
            if i<10:
                with open(self.path + crawl_date + "/" + category + "/" + category + "_0" + str(i) + ".json",'w') as outfile:
                    outfile.write(response.text)
            else :
                with open(self.path + crawl_date + "/" + category + "/" + category + "_" + str(i) + ".json",'w') as outfile:
                    outfile.write(response.text)

            print("category : " + category)
            print("page: " + str(i))
            skip = skip + 100




run().get_items()

