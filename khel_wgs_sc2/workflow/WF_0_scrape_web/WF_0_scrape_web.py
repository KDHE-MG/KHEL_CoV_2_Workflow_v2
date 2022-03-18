from workflow.WF_0_scrape_web.WF_0_helpers import WorkflowObj0
import json
import os



def run_script_0(run_ids):
    print("\n================================\nScrape Web Script\n================================\n\n")
    
    #creating WorkflowObj
    data_obj = WorkflowObj0()
    #getting info
    data_obj.get_json()

    #save run info into var, while downloading fasta files for each run id supplied
    run_info=data_obj.scrape(run_ids)
    

    #save run info from var into json file, with name Runid_RunID.json
    script_dir = "/".join(os.path.abspath(__file__).split('/')[:-4])
    rel_path = "/data/run_data.json"
    abs_path = script_dir + rel_path
    with open (abs_path,"w") as j_dump:
        run_info = json.dumps(run_info)
        j_dump.write(run_info)
    
    data_obj.close_conns()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")

#return run file location
 

 