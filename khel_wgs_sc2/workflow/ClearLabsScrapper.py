import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time 
import sys


class ClearLabsApi():

	def __init__(self, ChromDriver_Path,DLoad_Path):
		opt = Options()
		opt.add_experimental_option("prefs", {
		  "download.default_directory": DLoad_Path,
		  "download.prompt_for_download": False,
		  "download.directory_upgrade": True,
		  "safebrowsing_for_trusted_sources_enabled": False,
		  "safebrowsing.enabled": False})

		opt.headless= True

		ChromeDriverPathSer=Service(ChromDriver_Path)


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

		for run in runIDs:
			
			self.driver.find_element(By.XPATH,'//h2[contains(.,"'+run+'")]').click()
			
			time.sleep(2)

			run_sample_info[run]=parse_run_data(self.driver.page_source)

			self.download_fasta()

			self.driver.find_element(By.XPATH,"//a[@href='/lab/runs']").click()
			

		return run_sample_info



	def download_fasta(self):

		print("download started")

		self.driver.find_element(By.ID,"cl-button-menu-toggle-download").click() # clikc on download

		self.driver.find_element(By.XPATH,"//div[contains(.,'Download All FASTA')]") 

		self.driver.find_element(By.XPATH,"//div[contains(@class,'sc-6wkgny-0 sc-1n4kxe3-1 iwyGgY kBSIHC')]").click() #clicks the download all fasta button but not great becuase only finds the first element not specfifc enough should be bulit to be more robust

		self.driver.find_element(By.ID,"cl-button-download-fasta-files-submit").click() # this triggers the ok button after you selected it
		#sleep can be removed but waiting for file to be downloaded 
		time.sleep(5)
		


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




	







