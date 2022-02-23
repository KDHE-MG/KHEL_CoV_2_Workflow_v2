from ..workflow_obj import workflow_obj
import tarfile


class Workflow0_5(workflow_obj):

    def __init__(self):
        self.id = "WF0_5"

    def get_json(self):
        super().get_json(0) #what does this need besides    

    def extract(runId):

        fastas= tarfile.open(self.fast_file_download_path+"\\"+runId+"\\"+runId+".fastas.tar")

        fastas.extractall(self.fast_file_download_path+"\\"+runId)

        fastas.close()