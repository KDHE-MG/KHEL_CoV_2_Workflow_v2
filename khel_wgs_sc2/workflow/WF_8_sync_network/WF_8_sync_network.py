import time
from workflow.WF_8_sync_network import WorkflowObj8

def run_script_8(run_id):
    print("\n================================\n Synch Network script\n================================\n\n")
    #create object
    data_obj = WorkflowObj8()
    #read in json
    data_obj.get_json()
    #Clean up folders/files and move them to their permante location
    data_obj.clean_up(run_id)



    print("\n================================\nSuccess! Script Finished.\n================================\n\n")
   