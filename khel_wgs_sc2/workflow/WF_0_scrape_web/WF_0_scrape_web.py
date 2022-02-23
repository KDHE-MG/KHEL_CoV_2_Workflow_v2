import time
from workflow.ClearLabsScrapper import ClearLabsApi
from workflow.WF_0_scrape_web.WF_0_helpers import WorkflowObj0
import json



def run_script_0(run_ids):
    print("\n================================\nScrap Web Script\n================================\n\n")
    
    #creating WorkflowObj
    data_obj = WorkflowObj0
    #getting info
    data_obj.get_json()

    #save run info into var, while downloading fasta files for each run id supplied
    
    run_info=data_obj.scrape(run_ids)
    

    #save run info from var into json file, with name Runid_RunID.json
    with open ("data/run_data.json","w") as j_dump:
        j_dump.write(run_info)

	
	print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)
#return run file location
    return str(data_obj.run_data_dump_path)+"RunDump_"+"_".join(run_ids)+".json"

 