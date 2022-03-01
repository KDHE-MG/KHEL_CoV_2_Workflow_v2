from ..workflow_obj import workflow_obj
from workflow.logger import Script_Logger
import os
import datetime

class WorkflowObj8(workflow_obj):

    def __init__ (self):
        self.id = "WF8"
        self.log = Script_Logger("WF8_Synch_Network")
        self.log.start_log("Initialization of WF_8 sucessful")


    def get_json(self):
        super().get_json(8)
        self.log.write_log("get_json","Argument passed 8")


    def clean_up(self,runID):
        # setup ssh connection to linux
        self.log.write_log("clean_up", "establishing connection to linux")
        super().setup_ssh()
        self.log.write_log("clean_up", "connection established")
        run_id = runID
        machine_num = run_id[4:6]
        run_date = datetime.datetime.strptime(run_id[7:17], '%Y-%m-%d').strftime("%m%d%y")
        day_run_num = int(run_id[-2:])
        folder_name = run_date + "." + str(machine_num) + "." + str(day_run_num) + "/"
        delete_dirs = []

        # check lock file - is the analysis still running?
        self.log.write_log("clean_up", "Checking that analysis is finished")
        lock_path = self.fasta_file_path + "lock_file.txt"
        if self.ssh_handler.check_file(lock_path):
            print("The analysis is still being run!  Check back in ten minutes.")
            raise ValueError("The analysis is still running.")
        self.log.write_log("clean_up", "The analysis is finished, proceeding with transfer of files.")
        
        # pull fasta/q files
        self.write_log("clean_up", "fetching fasta/q files")
        linux_dir = self.fasta_file_path + "run_data/" + folder_name + "FAST files/"
        win_dir = self.network_destination + "Run Data/ClearLabs/" + folder_name + "FAST files/"
        self.ssh_handler.receive_files(linux_dir, win_dir)
        delete_dirs.append(linux_dir)
        self.write_log("clean_up", "fetch finished.")

        # pull concatenated fasta, nextclade, pangolin
        self.write_log("clean_up", "fetching results files")
        linux_dir = self.fasta_file_path + "run_data/" + folder_name
        win_dir = self.network_destination + "Run Data/ClearLabs/" + folder_name
        self.ssh_handler.receive_files(linux_dir, win_dir)
        delete_dirs.append(linux_dir)
        self.write_log("clean_up", "fetch finished.")

        # pull epi
        self.write_log("clean_up", "fetching epi files")
        linux_dir = self.fasta_file_path + "Results/" + run_date + "/"
        win_dir = self.network_destination + "Results/" + run_date + "/"
        self.ssh_handler.receive_files(linux_dir, win_dir)
        delete_dirs.append(linux_dir)
        self.write_log("clean_up", "fetch finished.")

        # pull GISAID files
        self.write_log("clean_up", "fetching GISAID files")
        linux_dir = self.fasta_file_path + "GISAID/" + run_date + "/"
        win_dir = self.network_destination + "GISAID/" + run_date + "/"
        self.ssh_handler.receive_files(linux_dir, win_dir)
        delete_dirs.append(linux_dir)
        self.write_log("clean_up", "fetch finished.")

        # delete files
        self.write_log("clean_up", "files being deleted from linux")
        for path in delete_dirs:
            for file in os.scandir(path):
                if file.is_file():
                    os.remove(file.path)
        self.write_log("clean_up", "deletion complete")
  