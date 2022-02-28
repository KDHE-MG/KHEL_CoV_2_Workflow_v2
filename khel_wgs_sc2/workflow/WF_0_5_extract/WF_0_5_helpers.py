from ..workflow_obj import workflow_obj
import tarfile
import os 
from logger import Script_Logger

class Workflow0_5(workflow_obj):

    def __init__(self):
        self.id = "WF0_5"
        self.log= Script_Logger("WFO_5_Extract")
        self.log.start_log("Initialization of WF_O_5 sucessful")

    def get_json(self):
        super().get_json(0) #what does this need besides    
        self.log.write_log("get_json","0 passed")

    def extract(self,runId):
        
        self.log.write_log("extract","Run ID passed "+runId)
        self.log.write_log("extract","Path to file is "+self.fasta_file_download_path+"/"+runId)
        
        fastas= tarfile.open(self.fast_file_download_path+"/"+runId+"/"+runId+".all.tar.gz")

        self.log.write_log("extract","Making Fasta File directory")
        os.mkdir(self.fast_file_download_path+"/"+runId+"/FAST files")
        
        self.log.write_log("extract","Performing Extraction")
        fastas.extractall(self.fast_file_download_path+"/"+runId+"/FAST files")

        fastas.close()