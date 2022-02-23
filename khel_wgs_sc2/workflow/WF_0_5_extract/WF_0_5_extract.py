from workflow.WF_0_5_extract.WF_0_5_helpers import Workflow0_5
import time

def run_scrip_0_5(runID):
    
    print("\n================================\nExtract Fasta Script\n================================\n\n")
    
    #creating WorkflowObj

    data_obj= Workflow0_5()

    data_obj.get_json()

    data_obj.extract(runID)


    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)