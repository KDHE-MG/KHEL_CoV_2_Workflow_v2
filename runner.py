import sys
import time
import subprocess

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            # call to main script
            subprocess.run("/home/ssh_user/miniconda3/envs/gen_workflow/bin/python /home/ssh_user/repos/KHEL_CoV_2_Workflow_v2/khel_wgs_sc2/khel_wgs_sc2.py")
        else:
            run_id = str(sys.argv[1])
            # call to main script
            subprocess.run("/home/ssh_user/miniconda3/envs/gen_workflow/bin/python /home/ssh_user/repos/KHEL_CoV_2_Workflow_v2/khel_wgs_sc2/khel_wgs_sc2.py " + run_id)
    except Exception as e:
        print(e)
        time.sleep(500)
