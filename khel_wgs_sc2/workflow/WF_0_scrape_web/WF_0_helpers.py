from ..workflow_obj import workflow_obj
from workflow.ClearLabsScrapper import ClearLabsApi
from logger import Script_Logger



class WorkflowObj0(workflow_obj):

    def __init__(self):
        self.id= "WF_0"
    

    def get_json(self):
        super().get_json(0)

    def scrape(self, runIds):
            
        #create webdriver object
        self.scrapper_obj = ClearLabsApi(self.chrome_driver_path, self.fasta_file_download_path)

        #Log into ClearLabs
        self.scrapper_obj.login(self.clearlabs_url,self.cl_user,self.cl_pwd)
        #extract run info and download corresponding fastas files
        run_dump= json.dumps(self.scrapper_obj.find_runs(runIds))

        #closing web browser
        self.scrapper_obj.driver.close()

        #returning run information in a dic 
            #structure {'RunID':{'SampleID':[position,sampleID, type of analysis, seq_coverage, assembly_coverage]}}
        return run_dump

    








	