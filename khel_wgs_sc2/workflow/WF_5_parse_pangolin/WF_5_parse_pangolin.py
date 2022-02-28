import time
import datetime
from workflow.WF_5_parse_pangolin.WF_5_helpers import WorkflowObj5

def run_script_5(run_id):
    print("\n================================\nRun Data Import Script\n================================\n\n")

    # import relevant data from json file
    data_obj = WorkflowObj5()
    data_obj.get_json()

    # the compiled fasta path will only be dependent on
    # the run_id.  Otherwise it will always be in the same
    # network location.  Use private_cache to store base path
    machine_num = run_id[4:6]
    run_date = datetime.datetime.strptime(run_id[7:17], '%Y-%m-%d').strftime("%m%d%y")
    day_run_num = int(run_id[-2:])
    file_name = "all_" + run_date + "_" + str(machine_num) + ".fasta"
    compiled_fasta_path =  data_obj.fasta_file_path + run_date + "." + str(machine_num) + "." + str(day_run_num) + "/"+ file_name

    # compute the paths needed to complete analysis
    data_obj.run_pangolin()
    pangolin_path = "/".join(compiled_fasta_path.split("/")[:-1])
    data_obj.get_pango_dfs(pangolin_path + "/results.csv")


    # push results to database
    data_obj.database_push()

    print("\n================================\nSUCCESS - END OF SCRIPT\n================================\n\n")
    time.sleep(2)

    

