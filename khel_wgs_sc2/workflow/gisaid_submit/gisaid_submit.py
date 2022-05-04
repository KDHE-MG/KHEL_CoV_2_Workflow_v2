from workflow.gisaid_submit.gisaid_submit_helper import gisaid_submit_obj



def run_gisaid_submit(runID):
    
    print("\n================================\nGISAID Submission\n================================\n\n")
    
    #creating WorkflowObj
    if input("Do you wish to submit to GISAID? (y or n) ").lower() == "y":
        
        print("GISAID submission will continue")
        
        data_obj= gisaid_submit_obj()

        data_obj.get_json()

        data_obj.submit(runID)
    else:
        print("Data will not be submitted to GISAID script will end")

 


    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
