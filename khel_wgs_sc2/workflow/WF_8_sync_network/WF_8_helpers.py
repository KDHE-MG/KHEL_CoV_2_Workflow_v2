from workflow import workflow_obj
from logger import Script_Logger
import os
import shutil

class WorkflowObj8(workflow_obj):

    def __init__ (self):
        self.id = "WF8"
        self.log = Script_Logger("WF8_Synch_Network")
        self.log.start_log("Initialization of WF_8 sucessful")


    def get_json(self):
        super.get_json(8)
        self.log.write_log("get_json","Argument passed 8")


    def clean_up(self,runID):
        #check that fasta files are still theire

        self.log.write_log("clean_up","Checking if Path to fasta exisit this path was passed     "+self.fasta_file_path+runID+"/Fasta file")
        if os.path.exists(self.fasta_file_path+runID+"/Fasta file") :
            shutil.move(self.fasta_file_path+runID, self.network_destintation)
            self.log.write_log("clean_up","files moved succesfully")
  

        else:
            self.log.write_warning("No Run Folder")