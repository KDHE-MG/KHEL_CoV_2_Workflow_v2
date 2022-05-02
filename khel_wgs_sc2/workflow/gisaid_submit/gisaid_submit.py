from workflow.gisaid_submit.gisaid_submit_helper import gisaid_submit_obj



def run_gisaid_submit(runID):
    
    print("\n================================\nGISAID Submission\n================================\n\n")
    
    #creating WorkflowObj

    data_obj= gisaid_submit_obj()

    data_obj.get_json()

    data_obj.submit(runID)

 


    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
