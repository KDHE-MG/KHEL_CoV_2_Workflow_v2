from ..workflow_obj import workflow_obj
from workflow.ClearLabsScrapper import ClearLabsApi
from logger import Script_Logger
import json
import os
import time


class WorkflowObj0(workflow_obj):

    def __init__(self):
        self.id= "WF_0"
    

    def get_json(self):
        super().get_json(0)

    def scrape(self, runIds):
        #create folder for fasta files
        os.mkdir(self.fasta_file_download_path+"\\"+runIds)

        #create webdriver object
        self.scrapper_obj = ClearLabsApi( self.fasta_file_download_path+"\\"+runIds)

        #Log into ClearLabs
        self.scrapper_obj.login(self.clearlabs_url,self.cl_user,self.cl_pwd)
        #extract run info and download corresponding fastas files
        run_dump= self.scrapper_obj.find_runs(runIds)

        #checking that compress file has downloaded before closing browswer
        self.download_wait(runIds)

        #closing web browser
        self.scrapper_obj.driver.close()

        #returning run information in a dic 
            #structure {'RunID':{'SampleID':[position,sampleID, type of analysis, seq_coverage, assembly_coverage]}}
        return run_dump


    def download_wait(self,runIds):

        download_complete = True

        while download_complete:

            if os.path.exists(self.fasta_file_download_path+"\\"+runIds+"\\"+runIds+".all.tar"):
                download_complete=False
                print("download completed")
                break
                
            time.sleep(5)

    








	