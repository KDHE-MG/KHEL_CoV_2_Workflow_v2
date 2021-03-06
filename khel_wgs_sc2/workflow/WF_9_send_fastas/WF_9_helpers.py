from ..workflow_obj import workflow_obj
import datetime


class WorkflowObj9(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_9"

    # methods
    def get_json(self):
        super().get_json(9)


    def get_lst_fasta_files(self, day):
        if not day:
            day = input("\nPlease enter the date for which you'd like to create a 'passed' fasta file formatted 'mm/dd/yyyy'\n--> ")
        self.day = datetime.datetime.strptime(day, "%m/%d/%Y")
        super().setup_db()
        fasta_lst_df = self.db_handler.sub_read(query=self.read_query_tbl1)
        fasta_lst_df =  fasta_lst_df[fasta_lst_df.wgs_run_date == self.day.strftime("%Y-%m-%d")]
        self.fasta_lst = fasta_lst_df["path_to_fasta"].values.astype(str).tolist()
        if len(self.fasta_lst) == 0:
            raise ValueError("==================================================================================\nError:\nNo eligible samples from this date!! - All samples failed QC?\n==================================================================================\n")


    def build_fasta(self, run_id):
        machine_num = run_id[4:6]
        run_date = datetime.datetime.strptime(run_id[7:17], '%Y-%m-%d').strftime("%m%d%y")
        day_run_num = int(run_id[-2:])
        folder_file = run_date + "." + str(machine_num) + "." + str(day_run_num) + "/" + self.day.strftime("%m%d%y") + "_epi.fasta"
        path_write = self.base_path + folder_file
        s=""
        ctr=0
        f = open(path_write, "w")
        for path in self.fasta_lst:
            curr_file = open(path, 'r')
            file_contents = curr_file.readlines()
            curr_file.close()
            s += "\n\n"
            for line in file_contents:
                s += line
            f.write(s)
            s=""
            print("finished with file ", ctr)
            ctr+=1
        f.close()





