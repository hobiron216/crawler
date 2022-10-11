import pendulum
import requests
import shutil
from pathlib import Path
import pytesseract
import cv2


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def ocr(image):
    img = cv2.imread(image)
    # gray = get_grayscale(img)
    # thresh = thresholding(gray)
    txt = pytesseract.image_to_string(img)

    return txt


def ocr2(image):
    img = cv2.imread(image)
    gray = get_grayscale(img)
    thresh = thresholding(gray)
    txt = pytesseract.image_to_string(thresh)

    return txt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'-l msa'

first_date = pendulum.datetime(2021, 6, 15)
end_date = pendulum.datetime(2021, 6, 17)

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


    if int(bulan)==6 and tahun==2020:
        if int (hari)==15 or int (hari) == 26:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-jun-2020/taburankes.jpg"
            url2 = ""
            url3 = ""
        else:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-jun-2020/taburankes.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-jun-2020/gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-jun-2020/gerak14hari02.jpg"

    elif int(bulan) == 7 :
        if int (hari) !=31:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-julai-2020/taburankes.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-julai-2020/gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-julai-2020/gerak14hari02.jpg"
        else:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-julai-2020/taburankes-all.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-julai-2020/taburankes-gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-julai-2020/taburankes-gerak14hari02.jpg"
    elif int(bulan) == 8 :
        if int(hari) ==20:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/082020/situasi-terkini-20-ogos-2020/taburankes-gerak14hari02.jpg"
            url2 = ""
            url3 = ""
        else :
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-ogos-2020/taburankes-all.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-ogos-2020/taburankes-gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-ogos-2020/taburankes-gerak14hari02.jpg"
    elif int(bulan) == 9 :
        if int(hari) == 2:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-septermber-2020/taburankes-all.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-septermber-2020/taburankes-gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-septermber-2020/taburankes-gerak14hari02.jpg"
        else:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-september-2020/taburankes-all.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-september-2020/taburankes-gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-september-2020/taburankes-gerak14hari02.jpg"
    elif int(bulan) == 10 :
        url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-oktober-2020/taburankes-all.jpg"
        url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-oktober-2020/taburankes-gerak14hari01.jpg"
        url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-oktober-2020/taburankes-gerak14hari02.jpg"
    elif int(bulan) == 11 :
        url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-november-2020/taburankes-all.jpg"
        url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-november-2020/taburankes-gerak14hari01.jpg"
        url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-november-2020/taburankes-gerak14hari02.jpg"
    elif int(bulan) == 12 :
        if int (hari) < 14 :
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-disember-2020/taburankes-all.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-disember-2020/taburankes-gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-" + str(hari) + "-disember-2020/taburankes-gerak14hari02.jpg"
        elif int (hari) == 26:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/122020/situasi-terkini-covid-19-di-malaysia-2612020/taburankes-all.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/122020/situasi-terkini-covid-19-di-malaysia-2612020/taburankes-gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/122020/situasi-terkini-covid-19-di-malaysia-2612020/taburankes-gerak14hari02.jpg"
        else:
            url1 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-covid-19-di-malaysia-" + str(hari) + str(bulan) + str(tahun) + "/taburankes-all.jpg"
            url2 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-covid-19-di-malaysia-" + str(hari) + str(bulan) + str(tahun) + "/taburankes-gerak14hari01.jpg"
            url3 = "http://covid-19.moh.gov.my/user/pages/02.terkini/"+ str(bulan) + "2020/situasi-terkini-covid-19-di-malaysia-" + str(hari) + str(bulan) + str(tahun) + "/taburankes-gerak14hari02.jpg"



    # print(url1,url2,url3)
    Path('/home/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/").mkdir(parents=True, exist_ok=True)
    Path('/home/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/").mkdir(parents=True, exist_ok=True)



    img1 = r'/home/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + '_img1.jpg'
    img2 = r'/home/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + '_img2.jpg'
    img3 = r'/home/covid19my/img/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + '_img3.jpg'

    if url1:
        response1 = requests.get(url1, stream=True)
        with open(img1, 'wb') as out_file:
            shutil.copyfileobj(response1.raw, out_file)
            out_file.close()
        ocr11 = ocr(img1)
        ocr12 = ocr2(img1)

        txt11 = r'/home/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img1.txt'
        txt12 = r'/home/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img1_modified.txt'

        with open(txt11, 'w') as outfile:
            outfile.write(ocr11)
            outfile.close()
        with open(txt12, 'w') as outfile:
            outfile.write(ocr12)
            outfile.close()

    if url2:
        response2 = requests.get(url2, stream=True)
        with open(img2, 'wb') as out_file:
            shutil.copyfileobj(response2.raw, out_file)
            out_file.close()
        ocr21 = ocr(img2)
        ocr22 = ocr2(img2)

        txt21 = r'/home/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img2.txt'
        txt22 = r'/home/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img2_modified.txt'

        with open(txt21, 'w') as outfile:
            outfile.write(ocr21)
            outfile.close()
        with open(txt22, 'w') as outfile:
            outfile.write(ocr22)
            outfile.close()

    if url3:
        response3 = requests.get(url3, stream=True)
        with open(img3, 'wb') as out_file:
            shutil.copyfileobj(response3.raw, out_file)
            out_file.close()
        ocr31 = ocr(img3)
        ocr32 = ocr2(img3)

        txt31 = r'/home/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img3.txt'
        txt32 = r'/home/covid19my/txt/' + str(tahun) + str(bulan) + str(hari) + "/" + str(tahun) + str(bulan) + str(hari) + 'img3_modified.txt'

        with open(txt31, 'w') as outfile:
            outfile.write(ocr31)
            outfile.close()
        with open(txt32, 'w') as outfile:
            outfile.write(ocr32)
            outfile.close()






    print(day)