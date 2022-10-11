import pendulum
import requests
import shutil
from pathlib import Path
# import pytesseract
import cv2
from pytesseract import image_to_string
from datetime import date
import datetime as datetime21

def telegram_bot_sendtext(bot_message):
    global response
    bot_token = '1381123927:AAEQ169ZfG5qQMvPaNaFyt8zBJzyeZ-feXc'
    bot_chatID = '1008898421'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    while True:
        try:
            response = requests.get(send_text, timeout=10)
            break
        except requests.exceptions.RequestException as e:
            print("gagal kirim telegram")
            continue

    return response.json()

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def ocr(image):
    img = cv2.imread(image)
    # gray = get_grayscale(img)
    # thresh = thresholding(gray)
    txt = image_to_string(img, lang='msa')

    return txt


def ocr2(image):
    img = cv2.imread(image)
    gray = get_grayscale(img)
    thresh = thresholding(gray)
    txt = image_to_string(thresh, lang='msa')

    return txt

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# custom_config = r'-l msa'
today = date.today()
crawl_date = today.strftime("%Y%m%d")
today_news = date.today() - datetime21.timedelta(1)

first_date = pendulum.datetime(today_news.year, today_news.month, today_news.day)
end_date = pendulum.datetime(today_news.year, today_news.month, today_news.day)
# first_date = pendulum.datetime(2021, 8, 21)
# end_date = pendulum.datetime(2021, 8, 23)

for day in pendulum.period(first_date, end_date).range('days'):
    hari = day.day

    bulan = day.month
    tahun = day.year

    # if int(bulan)==2:
    #     continue
    if int(hari) < 10:
        hari = "0" + str(hari)
    if int(bulan) < 10:
        bulan = "0" + str(bulan)

    url1 = "http://covid-19.moh.gov.my//user/pages/02.terkini/01.2021/" + str(bulan) + "." + str(bulan) + "/situasi-terkini-covid-19-di-malaysia-" + str(hari) + str(bulan) + str(tahun) + "/taburankes-all.jpg"
                                       # /user/pages/02.terkini/01.2021/07.07                                /situasi-terkini-covid-19-di-malaysia-19072021/taburankes-all.jpg
    url2 = "http://covid-19.moh.gov.my//user/pages/02.terkini/01.2021/" + str(bulan) + "." + str(
        bulan) + "/situasi-terkini-covid-19-di-malaysia-" + str(hari) + str(bulan) + str(
        tahun) + "/taburankes-gerak14hari01.jpg"
    url3 = "http://covid-19.moh.gov.my//user/pages/02.terkini/01.2021/" + str(bulan) + "." + str(
        bulan) + "/situasi-terkini-covid-19-di-malaysia-" + str(hari) + str(bulan) + str(
        tahun) + "/taburankes-gerak14hari02.jpg"

    # print(url1,url2,url3)
    Path('/news_cn/requests/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/").mkdir(parents=True, exist_ok=True)
    Path('/news_cn/requests/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/").mkdir(parents=True, exist_ok=True)



    img1 = '/news_cn/requests/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + '_img1.jpg'
    img2 = '/news_cn/requests/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + '_img2.jpg'
    img3 = '/news_cn/requests/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + '_img3.jpg'

    while True:
        try:
            response1 = requests.get(url1, stream=True, timeout=10)
            break
        except:
            continue
    with open(img1, 'wb') as out_file:
        shutil.copyfileobj(response1.raw, out_file)
        out_file.close()

    while True:
        try:
            response2 = requests.get(url2, stream=True, timeout=10)
            break
        except:
            continue
    with open(img2, 'wb') as out_file:
        shutil.copyfileobj(response2.raw, out_file)
        out_file.close()
    while True:
        try:
            response3 = requests.get(url3, stream=True, timeout=10)
            break
        except:
            continue
    with open(img3, 'wb') as out_file:
        shutil.copyfileobj(response3.raw, out_file)
        out_file.close()

    ocr11 = ocr(img1)
    ocr12 = ocr2(img1)
    ocr21 = ocr(img2)
    ocr22 = ocr2(img2)
    ocr31 = ocr(img3)
    ocr32 = ocr2(img3)

    txt11 = '/news_cn/requests/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img1.txt'
    txt12 = '/news_cn/requests/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img1_modified.txt'

    txt21 = '/news_cn/requests/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img2.txt'
    txt22 = '/news_cn/requests/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img2_modified.txt'

    txt31 = '/news_cn/requests/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img3.txt'
    txt32 = '/news_cn/requests/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img3_modified.txt'

    with open(txt11, 'w',  encoding='utf_8') as outfile:
        outfile.write(ocr11)
        outfile.close()
    with open(txt12, 'w',  encoding='utf_8') as outfile:
        outfile.write(ocr12)
        outfile.close()
    with open(txt21, 'w',  encoding='utf_8') as outfile:
        outfile.write(ocr21)
        outfile.close()
    with open(txt22, 'w',  encoding='utf_8') as outfile:
        outfile.write(ocr22)
        outfile.close()
    with open(txt31, 'w',  encoding='utf_8') as outfile:
        outfile.write(ocr31)
        outfile.close()
    with open(txt32, 'w',  encoding='utf_8') as outfile:
        outfile.write(ocr32)
        outfile.close()



    print(day)


message = "Engine : Covid19my \n Date : " + str(day)
telegram_bot_sendtext(str(message))
