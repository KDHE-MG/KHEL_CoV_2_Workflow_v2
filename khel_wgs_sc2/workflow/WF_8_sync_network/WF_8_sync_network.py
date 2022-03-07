from workflow.WF_8_sync_network.WF_8_helpers import WorkflowObj8

def run_script_8():
    print("\n================================\n Sync Network script\n================================\n\n")
    #create object
    data_obj = WorkflowObj8()
    #read in json
    data_obj.get_json()
    #Clean up folders/files and move them to their permante location
    data_obj.clean_up()



    print("\n================================\nSuccess! Script Finished.\n================================\n\n")
   