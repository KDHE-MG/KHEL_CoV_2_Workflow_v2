from workflow.WF_6_build_epi_report.WF_6_build_epi_report_helpers import WorkflowObj6
import time
import datetime

def run_script_6(run_id):
    # Print welcome message
    print("\n================================\nReport Generator\n================================\n\n")
    
    # import relevant data from json file
    data_obj = WorkflowObj6()
    data_obj.get_json()

    # open sql database --> pandas dataframe
    if run_id == "windows":
        data_obj.get_ui()
    else:
        run_date = run_id[7:17]
        data_obj.get_report(run_date)

    # get user input (should we format df by facility or date?)
    data_obj.get_df()

    # format the data, create the dataframe
    data_obj.format_df()

    # write out the dataframe to excel file
    data_obj.write_epi_report()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)
