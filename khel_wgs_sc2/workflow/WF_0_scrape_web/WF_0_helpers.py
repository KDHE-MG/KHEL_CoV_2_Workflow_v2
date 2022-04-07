from ..workflow_obj import workflow_obj
from workflow.ClearLabsScrapper import ClearLabsApi
from workflow.logger import Script_Logger
import datetime
import os
import time



class WorkflowObj0(workflow_obj):

    def __init__(self):
        self.id= "WF_0"
        self.log = Script_Logger("WF0_Scrape_Clear_Labs")
        self.log.start_log("Initialization of WF_O_sucessful")    

    def get_json(self):
        super().get_json(0)
        self.log.write_log("get_json","Argument passed was 0")

    def scrape(self, runId):
        #create folder for fasta files
        self.log.write_log("Scrape","Was run with the following runID passed "+runId)


        machine_num = runId[4:6]
        run_date = datetime.datetime.strptime(runId[7:17], '%Y-%m-%d').strftime("%m%d%y")
        day_run_num = str(int(runId[-2:]))
        runIds = run_date + "." + machine_num + "." + day_run_num
        self.log.write_log("Scrape- MkDIR","Creating new folder to store fasta and fasta q files with the following path "+self.fasta_file_download_path+"/"+runIds)
        
        if not os.path.exists(self.fasta_file_download_path+runIds):
            os.mkdir(self.fasta_file_download_path+runIds)

        #create webdriver object
        self.log.write_log("Scrape - Scrapper Obj","Initializing Scrapping Object")
        self.scrapper_obj = ClearLabsApi(self.fasta_file_download_path+runIds)

        self.log.write_log("Scrape - Login", "Loging into clearlabs")
        #Log into ClearLabs
        self.scrapper_obj.login(self.clearlabs_url,self.cl_user,self.cl_pwd)
        
        self.log.write_log("Scrape - Find Runs", "Downloading Fasta anf Fastaq files")
        #extract run info and download corresponding fastas files
        run_dump= self.scrapper_obj.find_runs(runId)

        #check if rundata is empty
        for key in [*run_dump]:
            if len(run_dump[key]) <= 1:
                    self.log.write_warning("Run_Info","Check ClearLabsScrapper Class Finder")
                    raise ValueError("Was not able to gather run info, CHECK CLEAR LABS SCRAPPER PY")

        #checking that compress file has downloaded before closing browswer
        self.log.write_log("Scrape Download Wait","Waiting for download to finish")
        self.download_wait(runId, runIds)


        self.log.write_log("Scrape - Closing Browswer","Closing")
        #closing web browser
        self.scrapper_obj.driver.close()

        #returning run information in a dic 
            #structure {'RunID':{'SampleID':[position,sampleID, type of analysis, seq_coverage, assembly_coverage]}}
        return run_dump


    def download_wait(self,runId, runIds):

        download_complete = True

        while download_complete:

            if os.path.exists(self.fasta_file_download_path+"/"+runIds+"/"+runId+".all.tar"):
                download_complete=False
                self.log.write_log("Download Wait","File Finshed Downloading")
                break
                
            time.sleep(10)
            self.log.write_log("Download Wait","Waiting on Download to finish")

    
    def close_conns(self):
        self.scrapper_obj.close_conns()







	
