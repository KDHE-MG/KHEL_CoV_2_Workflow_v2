import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time 
import datetime
from pathlib import Path


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
		self.driver.find_element_by_css_selector('li.sc-cd5qzr-0:nth-child(5) > a:nth-child(1) > span:nth-child(1)').click()

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

		self.driver.find_element(By.ID,"cl-button-menu-toggle-download").click() # clikc on download

		#self.driver.find_element(By.XPATH,"//div[contains(.,'Download All FASTA and FASTQ files')]") 
		#selecting download all fasta and fastaq files

		self.driver.find_element(By.CSS_SELECTOR,"div.sc-1n4kxe3-1:nth-child(3)").click() 

		#self.driver.find_element(By.XPATH,"//div[contains(@class,'sc-6wkgny-0 sc-1n4kxe3-1 iwyGgY kBSIHC')]").click() #clicks the download all fasta button but not great becuase only finds the first element not specfifc enough should be bulit to be more robust

		self.driver.find_element(By.ID,"cl-button-download-fasta-files-submit").click() # this triggers the ok button after you selected it
		
		# check the progress of the file download
		self.driver.execute_script("window.open()")
		self.driver.switch_to.window(self.driver.window_handles[-1])
		self.driver.get("chrome://downloads")
		file_name = "/home/ssh_user/WGS_Sequencing_COVID/run_data/temp.txt"
		# clear the file for this run
		with open(file_name, 'w') as f:
			f.write("")

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


		while True:
			try:
				time.sleep(30)
				# check file size
				try:
					sz = (Path(d_file_name).stat().st_size)/1000000 # divide by 10^6 to get Mb from bytes
				except Exception:
					break
				download_percentage = round((sz/full_size)*100, 2)
				with open(file_name, "a") as f:
					f.write("\nThe file is at: " + str(download_percentage) + "%" + " as of " + datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S"))
			except Exception as e:
				pass
		
		#sleep can be removed but waiting for file to be downloaded 
		time.sleep(5)
		
		
	def  close_conns(self):
		self.driver.quit()

def parse_run_data(run_html):

	run_page= bs(run_html,"html.parser")
	
	#finds all samples

	#run_samples= bs.find_all("div", class_="sc-i7x0dw-0 fFrize sc-10cusfd-0 fTCUMn")

	sample_info={}

	for item in run_page.find_all("div", class_="sc-i7x0dw-0 fFrize sc-10cusfd-0 fTCUMn"):
	#[position,sampleID, type of analysis, se_coverage,assembly_coverage]

		sample_info[item.find(class_="sc-1ibd7ul-0 daFoK sc-10cusfd-1 gLXtVh").text] = [ item.find(class_="sc-1ibd7ul-0 daFoK sc-10cusfd-1 kyGmtC").text ,item.find(class_="sc-1ibd7ul-0 daFoK sc-10cusfd-1 gLXtVh").text,
		item.find(class_="sc-1ibd7ul-0 daFoK sc-10cusfd-1 gLXuaL").text, item.find(class_="sc-1ibd7ul-0 daFoK sc-10cusfd-1 gLXuaj").text,  item.find(class_="sc-1ibd7ul-0 daFoK sc-10cusfd-1 gLXtZy").text  ]



	return sample_info






	







