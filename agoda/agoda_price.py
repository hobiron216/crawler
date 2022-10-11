import sys
import glob
import requests
from requests.structures import CaseInsensitiveDict
import os
import pandas as pd
from pathlib import Path
import json
import re
# df = pd.read_csv(r'/home/crawler/otc/agoda/agoda_total_hotel.csv')
url = "https://www.agoda.com/api/cronos/property/BelowFoldParams/RoomGridData"


df = pd.read_csv(r'/home/crawler/otc/agoda/Travel_destinations_in_Malaysia_Total.csv')
total_hotel = 0
total_data = 0
for region in df.values:
    region_name = region[0]
    json_dir_name = '/dataph/one_time_crawling/home/agoda2/20211220/' + region_name

    json_pattern = os.path.join(json_dir_name, '*_*_detail.json')
    file_list = glob.glob(json_pattern)
    for file in file_list:
        total_data = total_data + 1
        id_hotel = file.split("/")[7]
        id_hotel = id_hotel.split("_")[0]
        print(id_hotel)
        if total_data<=1270:
            continue
        # print(file)
        with open(file,'r', encoding='utf_8_sig') as data_json:
            try:
                data_json = json.load(data_json)
            except:
                continue
            nama_hotel = re.sub('[^A-Za-z0-9-]+', ' ', data_json["hotelInfo"]["name"])
            nama_hotel = nama_hotel.strip().replace(" ", "-").encode("ascii", "ignore").decode().replace("---","-").replace("--","-").replace("----","-").replace("-----","-")
            cityname = data_json["hotelInfo"]["address"]["cityName"].replace(" ", "-").encode("ascii", "ignore").decode()
            print(nama_hotel)
            print(cityname)

        headers = CaseInsensitiveDict()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
        headers["Accept"] = "application/json"
        headers["Referer"] = "https://www.agoda.com/%s/hotel/%s-my.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1844104&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2022-01-20&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=MYR&isFreeOccSearch=false&isCityHaveAsq=false&los=1&searchrequestid=5c087831-a39a-4000-bc20-76967a6b2400"%(nama_hotel,cityname)
        headers["Accept-Language"] = "en-US,en;q=0.5"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        headers["X-Requested-With"] = "XMLHttpRequest"
        headers["Content-type"] = "application/json; charset=utf-8"
        headers["AG-Language-Locale"] = "en-us"
        headers["AG-Language-Id"] = "1"
        headers["CR-Currency-Id"] = "4"
        headers["CR-Currency-Code"] = "RM"
        headers["Origin"] = "https://www.agoda.com"
        headers["DNT"] = "1"
        headers["Connection"] = "keep-alive"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = "same-origin"
        headers["TE"] = "trailers"

        data = '{"SearchType":4,"ObjectID":%s,"CheckIn":"2022-01-20T00:00:00","Origin":"MY","LengthOfStay":1,"Adults":2,"Children":0,"Rooms":1,"IsEnableAPS":false,"RateplanIDs":[],"PlatformID":0,"CurrencyCode":"RM","ChildAgesStr":null,"ConnectedTrip":false,"HashId":"","FlightSearchCriteria":{"CabinType":4},"PackageToken":null,"SessionId":"4xwqjjw1kgrkqgegykrh5ppv","multiHotelNextCriteria":null,"PriceView":1,"IsWysiwyp":true,"PollTimes":1}'%id_hotel
        while True:
            try:
                resp = requests.post(url, headers=headers, data=data, timeout=10)
                break
            except requests.exceptions.RequestException as e:
                print("connetion timeout")
                continue


        Path("/dataph/one_time_crawling/home/agoda2/price2/" +  region_name + "/").mkdir(parents=True,
                                                                                               exist_ok=True)
        with open("/dataph/one_time_crawling/home/agoda2/price2/" +  region_name + "/" + str(id_hotel) + "_price.json", 'w', encoding='utf_8_sig') as outfile:
            outfile.write(resp.text)

        print("total hotel : ", total_data)

