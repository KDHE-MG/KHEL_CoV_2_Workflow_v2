from ..workflow_obj import workflow_obj
import tarfile
import os 
import datetime
from workflow.logger import Script_Logger

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
        machine_num = runId[4:6]
        run_date = datetime.datetime.strptime(runId[7:17], '%Y-%m-%d').strftime("%m%d%y")
        day_run_num = str(int(runId[-2:]))
        runIds = run_date + "." + machine_num + "." + day_run_num
        self.log.write_log("extract","Path to file is "+self.fasta_file_download_path+"/"+runIds)
        
        fastas= tarfile.open(self.fasta_file_download_path+runIds+"/"+runId+".all.tar")

        self.log.write_log("extract","Making Fasta File directory")
        os.mkdir(self.fasta_file_download_path+runIds+"/FAST files")
        
        self.log.write_log("extract","Performing Extraction")
        fastas.extractall(self.fasta_file_download_path+runIds+"/FAST files")
        fastas.close()
        os.remove(self.fasta_file_download_path + runIds + "/"+runId+".all.tar")

        