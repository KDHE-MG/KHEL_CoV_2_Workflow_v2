import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import  datetime
import time 
import sys
import os


class ClearLabsApi():

	def __init__(self, DLoad_Path):
		self.DLoad_Path = DLoad_Path
		opt = Options()
		opt.add_experimental_option("prefs", {
		  "download.default_directory": DLoad_Path,
		  "download.prompt_for_download": False,
		  "download.directory_upgrade": True,
		  "safebrowsing_for_trusted_sources_enabled": False,
		  "safebrowsing.enabled": False})

		opt.headless= True
#chrome must be install on device runing this
#we should inculde the chrome binarys into resourses
		
		ChromeDriverPathSer=Service("/home/ssh_user/repos/KHEL_CoV_2_Workflow_v2/resources/chromedriver")

		self.driver = webdriver.Chrome(service=ChromeDriverPathSer,options=opt)
		self.driver.implicitly_wait(15)


	def login(self,LoginUrl,email, password): #logs you into the website

		self.driver.get(LoginUrl)
	
		self.driver.find_element(By.ID,"cl-field-login-email").send_keys(email)
		self.driver.find_element(By.ID,"cl-field-password-email").send_keys(password)	
		self.driver.find_element(By.ID,"cl-button-login-submit").click()

		print("done")

	def find_runs(self,runIDs):
		#change page to list of run pages
		self.driver.find_element(By.XPATH,"//a[@href='/lab/runs']").click() 

		run_sample_info={}

		#for run in runIDs:
			
		self.driver.find_element(By.XPATH,'//h2[contains(.,"'+runIDs+'")]').click()
			
		time.sleep(2)

		run_sample_info[runIDs]=parse_run_data(self.driver.page_source)

		self.download_fasta(run_sample_info[runIDs])

		self.driver.find_element(By.XPATH,"//a[@href='/lab/runs']").click()
			

		return run_sample_info



	def download_fasta(self, dict):

		print("download started")

		self.driver.find_element(By.ID,"cl-button-menu-toggle-icon-assets--file--download").click() # clikc on download

		
		#selecting download all fasta and fastaq files
		#self.driver.find_element(By.CSS_SELECTOR,"div.sc-1n4kxe3-1:nth-child(3)").click() 
		self.driver.find_element(By.XPATH,"//*[@id=\"app\"]/div/div[3]/div[1]/div[1]/div/header/section/div/div[2]/div/div[3]").click()


		self.driver.find_element(By.ID,"cl-button-download-fasta-files-submit").click() # this triggers the ok button after you selected it
		
		# check the progress of the file download
		#file_name = "/home/ssh_user/WGS_Sequencing_COVID/run_data/temp.txt"
		# clear the file for this run
		#with open(file_name, 'w') as f:
		#	f.write("")

		# estimate size of file to be downloaded
		full_size = 0
		for hsn in dict:
			full_size += (int(dict[hsn][3][:-1]) * 0.02626647847)
		full_size = int(full_size) # will be in Mb

		# find new, downloading file
		run_date = datetime.datetime.strptime(self.DLoad_Path.split("/")[-1].split(".")[0], "%m%d%y")
		machine_num = self.DLoad_Path.split("/")[-1].split(".")[1]
		day_run_num = self.DLoad_Path.split("/")[-1].split(".")[2]
		run_id = "BB1L" + machine_num + "." + run_date.strftime("%Y-%m-%d") + ".0" + str(int(day_run_num))
		d_file_name = self.DLoad_Path + "/" + run_id + ".all.tar.crdownload"


		#while True:
		#	try:
		#		time.sleep(30)
				# check file size
		#		try:
		#			sz = (Path(d_file_name).stat().st_size)/1000000 # divide by 10^6 to get Mb from bytes
		#		except Exception:
		#			break
		#		download_percentage = round((sz/full_size)*100, 2)
		#		with open(file_name, "w") as f:
		#			f.write("\nThe file is at: " + str(download_percentage) + "%" + " as of " + datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S"))
		#	except Exception as e:
		#		pass
		
		#sleep can be removed but waiting for file to be downloaded 
		time.sleep(5)
		
		
	def  close_conns(self):
		self.driver.quit()

def parse_run_data(run_html):

	run_page= bs(run_html,"html.parser")
	
	#finds all samples

	#run_samples= bs.find_all("div", class_="sc-i7x0dw-0 fFrize sc-10cusfd-0 fTCUMn")

	sample_info={}

	for item in run_page.find_all("div", class_="sc-4fik4j-0 kvrlUi sc-1d58pfg-0 zGyGo"):
	#[position,sampleID, type of analysis, se_coverage,assembly_coverage]
		if item.find(class_="sc-1ydgn5o-0 hPGlkS sc-1d58pfg-1 jyopXL").text != "—":
			#print(item.find(class_="sc-1ydgn5o-0 ixOnpe sc-1cxzq9f-1 ajslC").text)
			#hsn: postion,hsn,analysus, seq cov, assem covm 
			sample_info[item.find(class_="sc-1ydgn5o-0 hPGlkS sc-1d58pfg-1 jyopXL").text] = [ item.find(class_="sc-1ydgn5o-0 hPGlkS sc-1d58pfg-1 eMqSuI").text ,item.find(class_="sc-1ydgn5o-0 hPGlkS sc-1d58pfg-1 jyopXL").text,item.find(class_="sc-1ydgn5o-0 hPGlkS sc-1d58pfg-1 jyoqaV").text, item.find(class_="sc-1ydgn5o-0 hPGlkS sc-1d58pfg-1 jyopSJ").text,  item.find(class_="sc-1ydgn5o-0 hPGlkS sc-1d58pfg-1 jyoqcg").text]


	#print(sample_info)
	return sample_info




if __name__ == "__main__":

	s = ClearLabsApi("")
	s.login("https://wgs.app.clearlabs.com/login","","")

	q= s.find_runs("BB1L")

	s.driver.close()

	print(q)


