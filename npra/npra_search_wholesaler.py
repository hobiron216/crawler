
from bs4 import BeautifulSoup
import time
import json
import requests
from pathlib import Path
# import urllib3
# import shutil
# http = urllib3.PoolManager()

# proxy = "42.1.62.73:8228"
# category = "manufacturer"
# category = "importer"
category = "wholesaler"
Path(category + "/search/").mkdir(parents=True,exist_ok=True)
proxies = {
  "http": "http://42.1.62.73:8228",
  "https": "https://42.1.62.73:8228",
}
#
#

#


headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://quest3plus.bpfk.gov.my',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://quest3plus.bpfk.gov.my/pmo2/index.php',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
}

# with open("manufacturers/manufacturers.json", 'r', encoding='utf8') as outfile:
#     companys= json.load(outfile)

with open(category + "/" + category + ".json", 'r', encoding='utf8') as outfile:
    companys= json.load(outfile)
except21=[]
data_dobel=[]

def product_information(soup):
    product_information=[]
    # print(soup)
    product_name = ""
    registration_no = ""
    holder = ""
    holder_address = ""
    manufacturer = ""
    manufacturer_address = ""
    importer = ""
    importer_address = ""
    phone_no=""

    divs = soup.findAll("tr")
    # print(len(divs))

    for div in divs:
        divs2= div.findAll("td")

        if "Product Name" in div.get_text() and "N/A" not in div.get_text() :
            z=0
            for div2 in divs2:
                z = z + 1
                if z==1:
                    if "Product Name" in div2.get_text() :
                        product_name = div2.get_text().split(" :")
                        product_name= product_name[1].strip()
                else:
                    if "Registration No" in div2.get_text():
                        registration_no = div2.get_text().split(" :")
                        registration_no= registration_no[1].strip()
        # elif "Registration No" in div:

        elif "Holder" in div.get_text() and "N/A" not in div.get_text():
            z = 0
            for div2 in divs2:
                z = z + 1
                if z == 1:
                    if "Holder" in div2.get_text():
                        holder = div2.get_text().split(" :")
                        holder = holder[1].strip()
                else:
                    if "Holder Address" in div2.get_text():
                        holder_address = div2.get_text().split(" :")
                        holder_address= holder_address[1].strip()
        # elif "Holder Address" in div:

        elif "Phone No" in div.get_text() and "N/A" not in div.get_text():
            z=0
            for div2 in divs2:
                z = z + 1
                if z == 1:
                    if "Phone No" in div2.get_text():
                        phone_no = div2.get_text().split(" :")
                        phone_no = phone_no[1].strip()
        elif "Manufacturer" in div.get_text() and "N/A" not in div.get_text():
            z = 0
            for div2 in divs2:
                z = z + 1
                if z == 1:
                    if "Manufacturer" in div2.get_text():
                        manufacturer = div2.get_text().split(" :")
                        manufacturer = manufacturer[1].strip()
                else:
                    if "Manufacturer Address" in div2.get_text():
                        manufacturer_address = div2.get_text().split(" :")
                        manufacturer_address = manufacturer_address[1].strip()
        elif "Importer" in div.get_text() and "N/A" not in div.get_text():
            z = 0
            for div2 in divs2:
                z = z + 1
                if z == 1:
                    if "Importer" in div2.get_text():
                        importer = div2.get_text().split(" :")
                        importer = importer[1].strip()
                else:
                    if "Importer Address" in div2.get_text():
                        importer_address = div2.get_text().split(" :")
                        importer_address= importer_address[1].strip()


    result = {
        "product_name" : product_name,
        "registration_no" : registration_no,
        "holder" : holder,
        "holder_address" : holder_address,
        "phone_no" : phone_no,
        "manufacturer" : manufacturer,
        "manufacturer_address" : manufacturer_address,
        "importer" : importer,
        "importer_address" : importer_address
    }

    # product_information.append(result)
    return result


def tabel (soup):
    tabel_data=[]
    divs = soup.findAll("tr")
    # print(len(divs))
    y=0
    for div in divs:
        y=y+1
        if y==1:
            continue
        divs2 = div.findAll("td")

        z = 0
        for div2 in divs2:
            z = z + 1
            if z == 2:
                tabel_data.append(div2.get_text())


    return tabel_data


def pdf(soup,category,category_tabel, company, registration_no) :
    tabel_data = []
    divs = soup.findAll("tr")
    path=""
    # print(len(divs))
    y = 0
    for div in divs:
        y = y + 1
        if y == 1:
            continue
        divs2 = div.findAll("td")

        z = 0
        for div2 in divs2:
            z = z + 1
            if z == 2:
                nama_pdf = div2.get_text()
                if nama_pdf:
                    url = div2.find("a").attrs.get("href").replace("https","http")
                    while True:
                        try:

                            response = requests.get(url, timeout=5)
                            break
                        except Exception as e:
                            print(e)
                            continue
                    path = category + "/search/pdf/" +category_tabel + "/" + company.strip() + "/" + registration_no +"/" + nama_pdf
                    Path(category + "/search/pdf/" +category_tabel + "/" + company.strip() + "/" + registration_no + "/").mkdir(parents=True, exist_ok=True)

                    try:
                        with open(path, 'wb') as out_file:
                            out_file.write(response.content)
                            out_file.close()
                    except:
                        nama_pdf = nama_pdf.encode('ascii', 'ignore')
                        path = category + "/search/pdf/" + category_tabel + "/" + company.strip() + "/" + registration_no + "/" + str(
                            nama_pdf)
                        with open(path, 'wb') as out_file:
                            out_file.write(response.content)
                            out_file.close()


                tabel_data.append(path)
    return tabel_data


a=0
# companys = ["Nature's Grace Marketing (M) Sdn. Bhd."]
for company in companys:
    # a=a+1
    # if a>=2:
    #     break
    time.sleep(1)
    data = []
    company21 = company['company_name']
    # company21 = company
    company = company21.split("Sdn.")
    company = company[0].split("(")
    company = company[0]

    if "Co." in company:
        company = company.split("Co.")
        company = company[0]
    if "Corporation" in company:
        company = company.split("Corporation")
        company = company[0]
    if "- Siklotron" in company:
        company = company.split(" - Siklotron")
        company = company[0]
    # if "." in company:
    #     company = company.split(".")
    #     company = company[0]
    if "\'" in company:
        company = company.split("\'")
        company = company[0]
    print(company)

    while True:
        try:
            r=requests.get("http://quest3plus.bpfk.gov.my/pmo2/content.php?func=search&term="+ company + "&type=3&cat=1", timeout=5)
            break
        except Exception as e:
            print(e)
            continue
    r = json.loads(r.text)
    print(r)
    id_company=""
    for s in r:
        id_company=s['id']
        break
    print(id_company)
    if id_company:
        data21 = {
        'func': 'search',
        # 'searchBy': '4', #manufacturers
        # 'searchBy': '5', #importer
        'searchBy': '3', #wholesale
        'searchTxt': str(id_company)    ,
        'cat': '1'
        }
        while True:
            try :
                response = requests.post('http://quest3plus.bpfk.gov.my/pmo2/content.php', headers=headers, data=data21, proxies=proxies, timeout=5)
                break
            except:
                print("gagal")
                continue
        # print(response.text)
        #
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        try :
            divs = soup.find("tbody").findAll("tr")
            i=0

            for div in divs:
                divs2 = div.findAll("td")
                i=i+1
                z=0

                for div2 in divs2:
                    z=z+1
                    if z==1:
                        continue
                    elif z==2:
                        registration_no = div2.get_text().strip()
                        url_detail = "http://quest3plus.bpfk.gov.my/pmo2/detail.php?type=product&id=" + registration_no
                        print(url_detail)
                        while True:
                            try:
                                response2 = requests.get(url_detail, headers=headers,proxies=proxies, timeout=5)
                                # response2 = http.request('GET', url_detail)
                                break
                            except:
                                print("gagal")
                                continue
                            # print(response.text)
                            #
                        html2 = response2.text
                        # print(html2)
                        soup2 = BeautifulSoup(html2, 'html.parser')
                        divs2 = soup2.findAll("div", class_="row")
                        # print(len(divs2))
                        # if len(divs2) > 4:
                        #     print(len(divs2))
                        #     for div2 in divs2:
                        #         print(div2.find("div", class_="alert alert-sm alert-border-left alert-primary").get_text())
                        product_information21 =""
                        ingredients_information21=""
                        packaging_information21=""
                        consumer=""
                        label_im=""
                        label_out=""
                        proposed=""
                        technical=""

                        for div2 in divs2:
                            # print(div2.get_text())
                            if "Product Information" in div2.get_text():
                                product_information21 = product_information(div2)
                                # print(product_information21)
                                # break
                            elif "Ingredients Information" in div2.get_text():
                                ingredients_information21 = tabel(div2)
                                # print(ingredients_information21)
                            elif "Packaging Information" in div2.get_text():
                                packaging_information21 = tabel(div2)
                                # print(packaging_information21)
                            elif "Consumer Medication Information Leaflet" in div2.get_text():
                                category_tabel = "Consumer Medication Information Leaflet"
                                consumer = pdf(div2, category, category_tabel, company , registration_no)
                                # print(consumer)
                            elif "Label (mock-up) for Immediate Container" in div2.get_text():
                                category_tabel = "Label (mock-up) for Immediate Container"
                                label_im = pdf(div2, category, category_tabel, company, registration_no)
                                # print(label_im)
                            elif "Label (mock-up) for Outer Carton" in div2.get_text():
                                category_tabel = "Label (mock-up) for Outer Carton"
                                label_out = pdf(div2, category, category_tabel, company, registration_no)
                                # print(label_out)

                            elif "Proposed Package Insert" in div2.get_text():
                                category_tabel = "Proposed Package Insert"
                                proposed = pdf(div2, category, category_tabel, company, registration_no)
                                # print(proposed)
                            elif "Technical Evaluation Summary" in div2.get_text():
                                category_tabel = "Technical Evaluation Summary"
                                technical =  pdf(div2, category, category_tabel, company, registration_no)
                                if not technical:
                                    technical=""
                                print(technical)

                        result = {
                            "product_information" : product_information21,
                            "ingredients_information" : ingredients_information21,
                            "packaging_information" : packaging_information21,
                            "consumer_mediation_information_leaflet" : consumer,
                            "label_(mock-up)_for_immediate_container" : label_im,
                            "label_(mock-up)_for_Outer_Carton" : label_out,
                            "proposed_package_insert" : proposed,
                            "technical_evaluation_summary" : technical,
                            "url" : url_detail
                        }

                        data.append(result)
                # if i>5:
                #     break
                    # print(data)
            with open(category + "/search/" + company.strip() + ".json", 'w', encoding='utf_8') as outfile:
                json.dump(data, outfile, ensure_ascii=False)


        except Exception as e:
            print(e)
            if company21 in except21:
                if company21 not in data_dobel:
                    data_dobel.append(company21)
                    continue
            else:
                except21.append(company21)
            # except21.append(company21)
            continue
                # break
    else:
        if company21 in except21:
            if company21 not in data_dobel:
                data_dobel.append(company21)

        else:
            except21.append(company21)



        # print(data)
        # break
        # with open(category + "/search/" + company + ".json", 'w', encoding='utf_8') as outfile:
        #     json.dump(data, outfile, ensure_ascii=False)

print(except21)
#
with open(category + "/" + category + "_except.json", 'w', encoding='utf_8') as outfile:
    json.dump(except21, outfile, ensure_ascii=False)



# with open("importers.json", 'w', encoding='utf_8') as outfile:
#     json.dump(data, outfile, ensure_ascii=False)
#
# with open("wholesalers.json", 'w', encoding='utf_8') as outfile:
#     json.dump(data, outfile, ensure_ascii=False)

#sample nama company sama = dksh malaysia wholesal