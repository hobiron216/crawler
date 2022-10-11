import sys

import PyPDF2
import os
import json
import glob
from pathlib import Path


def personal(strs):
	personal_data = []
	personal_information = strs.split("Personal Information")[1]
	personal_information = personal_information.split("Work experience")[0]

	name = personal_information.split("Name")[1]
	name = name.split("City")[0]
	city = personal_information.split("City")[1]
	city = city.split("ZIP")[0]
	zip = personal_information.split("ZIP/Postal Code")[1]
	zip = zip.split("State")[0]
	state = personal_information.split("State")[1]
	state = state.split("Date")[0]
	date = personal_information.split("Date of Birth")[1]
	date = date.split("Gender")[0]

	gender = personal_information.split("Gender")[1]
	gender = gender.split("E-mail")[0]

	email = personal_information.split("E-mail")[1]
	email = email.split("Telephone")[0]

	telephone = personal_information.split("Telephone number")[1]
	telephone = telephone.split("|")[0]
	try:
		print(telephone)
	except:
		telephone = telephone.split("Education")[0]

	result = {
		"name": name,
		"city": city,
		"zip": zip,
		"state": state,
		"date_of_birth": date,
		"gender": gender,
		"email": email,
		"telephone": telephone
	}




	return result

list_category = ["Jr_Programmer", "BUSINESS_ANALYST", "MANDARIN_JOURNALIST", "SENIOR_RESEARCH_ASSISTANT", "JOURNALIST", "Internship_Mandarin_Journalist", "APACHE_SPARK_DEVELOPER", "INTERNSHIP_JOURNALIST"]
pdf_gagal = []
for category in list_category:

	a=0
	Path("/dataph/one_time_crawling/home/myfuturejob/parsing_pdf3/" + category + "/").mkdir(parents=True,																				 exist_ok=True)
	json_dir_name = '/dataph/one_time_crawling/home/myfuturejob/20211221/' + category + "/"

	json_pattern = os.path.join(json_dir_name, '*_cv.pdf')
	file_list = glob.glob(json_pattern)
	for file in file_list:

		# if file !="/dataph/one_time_crawling/home/myfuturejob/20211221/APACHE_SPARK_DEVELOPER/e8a4b77a-f4f5-4963-97b5-fad23b1745f8_cv.pdf":
		# 	continue
		print(file)
		# df_xls1= spark.read.csv(root + file , header= True,  nullValue="", encoding = 'UTF-8')
		pdfFileObj = open(file, 'rb')
		# print(pdfFileObj)
		# file2 = file.replace(".pdf","")
		# print(file2)
		# print(cat)
		# /home/amel/parlimen/pdf/20210910/Jawapan Lisan
		# /home/amel/parlimen/pdf/20210910/Pernyata Resmi

		# creating a pdf reader object
		try:
			pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		except:
			pdf_gagal.append(file)
			continue

		# # printing number of pages in pdf file
		# print(pdfReader.numPages)

		# #looping page
		# # creating a page object
		i = 0
		pdf_pages = []
		for i in range (0,pdfReader.numPages) :
			try :
				pageObj = pdfReader.getPage(i)
				pageExtract = pageObj.extractText()
				pdf_pages.append(pageExtract)
			except :
				print("page : "+str(i))
				print("File : "+file)
		strs = " "
		strs = strs.join(pdf_pages)
		strs = str(strs).strip().replace("\n", "|").replace("\\n", "|").replace("\"[","").replace("]\"","")


		# print(result_pdf)

		last_position = ""
		last_employer = ""
		personal_information =""
		work_experience = ""
		profesional_certification = ""
		education = ""
		languages = ""
		driver_license = ""
		training = ""
		reference = ""


		try:
			last_position = strs.split("Last position:")[1]
			last_position = last_position.split("Last employer:")[0].strip()

			last_employer = strs.split("Last employer:")[1]
			last_employer = last_employer.split("0")[0].strip()
		except:
			pass

		try:
			print(last_position)
		except:
			last_position = last_position.split("0")[0]
			print(last_position)
			# print(last_employer)

		# print(last_employer)
		# continue

		personal_information = personal(strs)

		if "Work experience" in strs:
			if "Professional Certification" in strs :
				work_experience = strs.split("Work experience")[1]
				work_experience = work_experience.split("Professional Certification")[0].replace("MYFutureJobs","")
			# for data_work in total_data_work:
				# 	print(data_work[1].encode('utf-8'))


				# break

			else:
				work_experience = strs.split("Work experience")[1]
				work_experience = work_experience.split("Education")[0].replace("MYFutureJobs","")
		else:
			work_experience = ""

		if "Professional Certification" in strs:
			profesional_certification = strs.split("Professional Certification")[1]
			profesional_certification = profesional_certification.split("Education")[0].replace("MYFutureJobs","").strip()

		education = strs.split("Education")
		if len(education) > 2:
			education = strs.split("Education")[-1]
		else:
			education = strs.split("Education")[1]
		education = education.split("Other Skills")[0]


		languages = strs.split("Languages")[1]
		languages = languages.split("Driver")[0].replace("MYFutureJobs","")

		driver_license = strs.split("License")[1]
		driver_license = driver_license.split("Skills")[0].replace("MYFutureJobs","")

		# skills = strs.split("License")[1]

		skills = strs.split("Skills")[2].replace("MYFutureJobs","")
		if "Training" in skills:
			skills = skills.split("Training")[0].replace("MYFutureJobs", "")
			training = strs.split("Training")[1].replace("MYFutureJobs", "")


		if "Reference" in strs:
			skills = skills.split("Reference")[0].replace("MYFutureJobs", "")
			if training:
				training = training.split("Reference")[0].replace("MYFutureJobs", "")
			reference = strs.split("Reference")[1].replace("MYFutureJobs", "")

		name_json = file.replace("_cv.pdf",".json")

		with open(name_json, "r", encoding='utf_8_sig') as outfile:
			data_json = json.load(outfile)

		result_pdf = {
			"general_data" : data_json,
			"last_position": last_position,
			"last_employer": last_employer,
			"personal_information" : personal_information,
			"work_experience" : work_experience,
			"profesional_certification" : profesional_certification,
			"education" : education,
			"languages" : languages,
			"driver_license" : driver_license,
			"skills" : skills,
			"training" : training,
			"reference" : reference,
			"path": file,
		}

		nama_file = file.split("/")[7].replace("_cv.pdf",".json")


		with open(r"/dataph/one_time_crawling/home/myfuturejob/parsing_pdf3/" + category + "/" + nama_file , 'w') as a : #path result
			json.dump(result_pdf, a)
		# break
			# with open(r"/home/amel/parlimen/20220103/PenyataRasmi/Result/"+file2+".txt", 'w') as a : #path result
		# break
			#     a.write(str(result_pdf))

		# break


		# pageObj = pdfReader.getPage(1)

		# # extracting text from page
		# print(pageObj.extractText())

		# with open(r"/home/amel/parlimen/pdf/20210910/Result/testpdf.txt", 'w') as a :
		#     a.write(str(pageObj.extractText()).strip().replace("\n", "|"))

		# # closing the pdf file object
		# pdfFileObj.close()

# print(a)
print(pdf_gagal)
print(len(pdf_gagal))