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

def work(strs):
	total_work_experience = ""
	date_job=""
	job=""
	position_level=""
	employer=""
	related_skills=""
	sector=""
	job_description=""
	data = []

	work_experience = strs
	work_experience21 = work_experience.split(" - ")[0]
	if "1 Month" in work_experience21:
		total_work_experience = work_experience21.split("Month")[0] + "Month"

	elif "Months" in work_experience21:
		total_work_experience = work_experience21.split("Months")[0] + "Months"
	else:
		if "1 Year" in work_experience:
			total_work_experience = work_experience21.split("Year")[0] + "Year"
		else:
			total_work_experience = work_experience21.split("Years")[0] + "Years"

	total_work_experience = total_work_experience.split("Total Work Experience:")[1].strip()
	total_data_work = work_experience.split(" - ")
	# print(len(total_data_work))
	# print(len(total_data_work))
	if len(total_data_work) > 2:
		for i in range(0, len(total_data_work)):
			if i == 0:
			# 	date_job = total_data_work[i] + " - " +  total_data_work[i+1].split(")")[0]
			# 	date_job = date_job.split(total_work_experience)[1] + ")"
			# 	# print(date_job)
				continue
			# date_job = total_data_work[i] + " - " + total_data_work[i + i].split(")")[0]
			# date_job = date_job.split(total_work_experience)[1] + ")"
			# print(total_data_work[i])
			if "1 month" in total_data_work[i]:
				# print("ini wkwkw :" +  i)
				titik = total_data_work[i].split("month)")
			elif "months" in total_data_work[i]:
				# print("ini wkwkw :" +  str(i))
				titik = total_data_work[i].split("months)")
			else:
				if "1 year" in total_data_work[i]:
					titik = total_data_work[i].split("year)")
				else:
					titik = total_data_work[i].split("years)")

			# try :

			try:
				titik = titik[1]
			except:
				titik = titik[0]
			# except:
			# 	print(total_data_work[i])
			# 	print(titik)
			# 	break
			# print(str(titik).encode())


			if titik:
				data_titik = titik
				job = data_titik.split("Employer")[0]
				# print(data_titik)
				employer = data_titik.split("Employer")[1]
				employer = employer.split("Position level")[0]
				position_level = data_titik.split("Position level")[1]
				position_level = position_level.split("Related skills")[0]
				related_skills = data_titik.split("Related skills")[1]
				related_skills = related_skills.split("Sector")[0]
				sector = data_titik.split("Sector")[1]
				sector = sector.split("Job description")[0]
				job_description = data_titik.split("Job description")[1]

				result = {
					"total_work_experience": total_work_experience,
					# "date_job": date_job,
					"job": job,
					"employer": employer,
					"position_level": position_level,
					"related_skills": related_skills,
					"sector": sector,
					"job_description": job_description
				}

				data.append(result)
	else:
		# try:
		# 	date_job = work_experience.split("Months")[1].split(")")[0] + ")"
		# except:
		# 	try:
		# 		date_job = work_experience.split("Month")[1].split(")")[0] + ")"
		# 	except:
		# 		try :
		# 			date_job = work_experience.split("Years")[1].split(")")[0] + ")"
		# 		except:
		# 			try:
		# 				date_job = work_experience.split("Year")[1].split(")")[0] + ")"
		# 			except:
		# 	return data
		try:
			job = work_experience.split(")")[1]
		except:
			date_job = ""
			result = {
				"total_work_experience": total_work_experience,
				# "date_job": date_job,
				"job": job,
				"employer": employer,
				"position_level": position_level,
				"related_skills": related_skills,
				"sector": sector,
				"job_description": job_description
			}
			data.append(result)
			return data
		job = job.split("Employer")[0]
		employer = work_experience.split("Employer")[1]
		employer = employer.split("Position level")[0]
		position_level = work_experience.split("Position level")[1]
		position_level = position_level.split("Related skills")[0]
		related_skills = work_experience.split("Related skills")[1]
		related_skills = related_skills.split("Sector")[0]
		sector = work_experience.split("Sector")[1]
		sector = sector.split("Job description")[0]
		job_description = work_experience.split("Job description")[1]

		result = {
			"total_work_experience": total_work_experience,
			# "date_job": date_job,
			"job": job,
			"employer": employer,
			"position_level": position_level,
			"related_skills": related_skills,
			"sector": sector,
			"job_description": job_description
		}

		data.append(result)
	return data

def work2(strs):
	total_work_experience = ""
	date_job = ""
	job = ""
	position_level = ""
	employer = ""
	related_skills = ""
	sector = ""
	job_description = ""
	data = []

	work_experience = strs
	work_experience21 = work_experience.split("-")[0]
	if "1 Month" in work_experience21:
		total_work_experience = work_experience21.split("Month")[0] + "Month"

	elif "Months" in work_experience21:
		total_work_experience = work_experience21.split("Months")[0] + "Months"
	else:
		if "1 Year" in work_experience:
			total_work_experience = work_experience21.split("Year")[0] + "Year"
		else:
			total_work_experience = work_experience21.split("Years")[0] + "Years"

	total_work_experience = total_work_experience.split("Total Work Experience:")[1].strip()
	total_data_work = work_experience.split(")")

	# print(str(total_data_work).encode("utf-8"))
	# print(len(total_data_work))
	# print(len(total_data_work))
	if len(total_data_work) > 2:
		for i in range(0, len(total_data_work)):
			if i == 0:
				date_job = total_data_work[i] + ")"

				continue



			titik = total_data_work[i]


			if titik:
				data_titik = titik
				job = data_titik.split("Employer")[0]
				employer = data_titik.split("Employer")[1]
				employer = employer.split("Position level")[0]
				position_level = data_titik.split("Position level")[1]
				position_level = position_level.split("Related skills")[0]
				related_skills = data_titik.split("Related skills")[1]
				related_skills = related_skills.split("Sector")[0]
				sector = data_titik.split("Sector")[1]
				sector = sector.split("Job description")[0]
				job_description = data_titik.split("Job description")[1]

				result = {
					"total_work_experience": total_work_experience,
					# "date_job": date_job,
					"job": job,
					"employer": employer,
					"position_level": position_level,
					"related_skills": related_skills,
					"sector": sector,
					"job_description": job_description
				}

				data.append(result)


	else:
		try:
			date_job = work_experience.split("Months")[1].split(")")[0] + ")"
		except:
			try:
				date_job = work_experience.split("Month")[1].split(")")[0] + ")"
			except:
				try:
					date_job = work_experience.split("Years")[1].split(")")[0] + ")"
				except:
					date_job = work_experience.split("Year")[1].split(")")[0] + ")"

		job = work_experience.split(")")[1]
		job = job.split("Employer")[0]
		employer = work_experience.split("Employer")[1]
		employer = employer.split("Position level")[0]
		position_level = work_experience.split("Position level")[1]
		position_level = position_level.split("Related skills")[0]
		related_skills = work_experience.split("Related skills")[1]
		related_skills = related_skills.split("Sector")[0]
		sector = work_experience.split("Sector")[1]
		sector = sector.split("Job description")[0]
		job_description = work_experience.split("Job description")[1]

		result = {
			"total_work_experience": total_work_experience,
			# "date_job": date_job,
			"job": job,
			"employer": employer,
			"position_level": position_level,
			"related_skills": related_skills,
			"sector": sector,
			"job_description": job_description
		}

		data.append(result)
	return data

def educ(strs):

	data =[]



	education21 = strs.split(" - ")
	if len(education21) > 2:
		for i in range(0, len(education21)):
			try :
				if i ==0 :
					continue
				# if i == 0:
				# 	date_education = education21[i] + " - " +  education21.split(")")[0]
				# 	date_education = date_education.split(education21)[1] + ")"
				# 	# print(date_job)
				# 	continue
				# date_education = education21[i] + " - " + education21[i + i].split(")")[0]
				# date_education = date_education.split(total_work_experience)[1] + ")"

				if "1 month" in education21[i]:
					split_all = education21[i].split("month)")

				elif "months" in education21[i]:

					split_all = education21[i].split("months)")


				else:
					if "1 year" in education21[i]:
						split_all = education21[i].split("year)")

					else:
						split_all = education21[i].split("years)")


				data_edu = split_all[1]

				try:
					field_of_study = data_edu.split("Field of Study")[1]
					field_of_study = field_of_study.split("Graduated")[0]
					education_name = data_edu.split("Field of Study")[0]
				except:
					field_of_study = ""
					education_name = data_edu.split("Graduated")[0]
				graduated = data_edu.split("Graduated")[1]
				if "Yes" in graduated:
					graduated = "Yes"
				elif "No" in graduated:
					graduated = "No"
				else:
					graduated = ""


				result = {
					# "date_education": date_education,
					"education_name": education_name,
					"field_of_study": field_of_study,
					"graduated": graduated

				}

				data.append(result)
			except:
				return data



	else:
		if "1 month" in strs:
			split_all = strs.split("month)")
			date_education = split_all[0] + "month"+ ")"
		elif "months" in strs:
			split_all = strs.split("months)")
			date_education = split_all[0] + "months" + ")"
		else:
			if "1 year" in strs:
				split_all = strs.split("year)")
				date_education = split_all[0] + "year" + ")"
			else:
				split_all = strs.split("years)")
				date_education = split_all[0] + "years"  + ")"


		try :
			data_edu = split_all[1]
		except:
			try :
				data_edu = strs.split("-")[1]
			except:
				return data
		# print(data_edu)

		try :
			field_of_study = data_edu.split("Field of Study")[1]
			field_of_study = field_of_study.split("Graduated")[0]
			education_name = data_edu.split("Field of Study")[0]
		except:
			field_of_study = ""
			education_name = data_edu.split("Graduated")[0]
		# print(data_edu)
		graduated = data_edu.split("Graduated")[1]
		if "Yes" in graduated:
			graduated = "Yes"
		elif "No" in graduated:
			graduated = "No"
		else:
			graduated = ""


		result = {
			# "date_education" : date_education,
			"education_name" : education_name,
			"field_of_study" : field_of_study,
			"graduated" : graduated

		}

		data.append(result)
	return data


a=0
Path("/dataph/one_time_crawling/home/myfuturejob/parsing_pdf/APACHE_SPARK_DEVELOPER/").mkdir(parents=True,																				 exist_ok=True)
json_dir_name = '/dataph/one_time_crawling/home/myfuturejob/20211221/APACHE_SPARK_DEVELOPER/'
cacad =[]
json_pattern = os.path.join(json_dir_name, '*_cv.pdf')
file_list = glob.glob(json_pattern)
for file in file_list:

		# if file !="/dataph/one_time_crawling/home/myfuturejob/20211221/APACHE_SPARK_DEVELOPER/551ab06c-34e1-4ddc-848d-9561d1d137da_cv.pdf":
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
				work_experience = work_experience.split("Professional Certification")[0]

				try :
					work_experience = work(work_experience)
				except:
					# work_experience = work2(work_experience)
					try :
						work_experience = work2(work_experience)
					except:
						cacad.append(file)
						work_experience = strs.split("Work experience")[1]
						work_experience = work_experience.split("Professional Certification")[0]
			# for data_work in total_data_work:
				# 	print(data_work[1].encode('utf-8'))


				# break

			else:
				work_experience = strs.split("Work experience")[1]
				work_experience = work_experience.split("Education")
				# print(str(work_experience).encode())
				if len(work_experience) > 2:
					# print("wkwkw")
					work_experience = work_experience[:-1]
					aw = ""
					work_experience = aw.join(work_experience)

				else:
					work_experience = work_experience[0]
				try:
					work_experience = work(work_experience)
				except:
					# work_experience = work2(work_experience)
					try:
						work_experience = work2(work_experience)
					except:
						cacad.append(file)
						work_experience = strs.split("Work experience")[1]
						work_experience = work_experience.split("Professional Certification")[0]
		else:
			work_experience = ""

		if "Professional Certification" in strs:
			profesional_certification = strs.split("Professional Certification")[1]
			profesional_certification = profesional_certification.split("Education")[0].replace("MYFutureJobs","").strip()

		education = strs.split("Education")

		# print(len(education))
		if len(education) > 2:
			# print("wkwkw")
			education = education[-1]

		else:
			education = education[1]

		# print(education.)

		education = education.split("Other Skills")[0]
		try:
			education = educ(education)
		except:
			try :
				education = strs.split("Professional Certification")[1]
				education = education.split("Education")[1]
				education = education.split("Other Skills")[0]
				# print(education.encode())
				education = educ(education)
			except:
				education = strs.split("Education")[1]
				education = education.split("Other Skills")[0]




		languages = strs.split("Languages")[1]
		languages = languages.split("Driver")[0]

		driver_license = strs.split("License")[1]
		driver_license = driver_license.split("Skills")[0]

		# skills = strs.split("License")[1]
		skills = strs.split("Skills")[2].replace("MYFutureJobs","")

		name_json = file.replace("_cv.pdf",".json")

		with open(name_json, "r", encoding='utf_8_sig') as outfile:
			data_json = json.load(outfile)

		result_pdf = {
			"general_data" : data_json,
			"last_position" : last_position,
			"last_employer" : last_employer,
			"personal_information" : personal_information,
			"work_experience" : work_experience,
			"profesional_certification" : profesional_certification,
			"education" : education,
			"languages" : languages,
			"driver_license" : driver_license,
			"skills" : skills,
			"path": file,
		}

		nama_file = file.split("/")[7].replace("_cv.pdf",".json")


		with open(r"/dataph/one_time_crawling/home/myfuturejob/parsing_pdf/APACHE_SPARK_DEVELOPER/" + nama_file , 'w') as a : #path result
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
print(cacad)
print(len(cacad))