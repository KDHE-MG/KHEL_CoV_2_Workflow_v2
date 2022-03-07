from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from ..formatter import add_cols, remove_pools, remove_blanks, merge_dataframes
import subprocess
from workflow.logger import Script_Logger


class WorkflowObj5(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_5"
        self.log = Script_Logger("WF_5_Parse_Pangolin")
        self.log.start_log("Initalization of WF5")

    # methods
    def get_json(self):
        super().get_json(5)
        self.log.write_log("get_json","Argument Pass 5")


    def get_pango_dfs(self, pango_path):
        self.log.write_log("get_pango_dfs","Starting")

        splt = pango_path.split("/")
        parent_folder = splt[-2]
        data = parent_folder.split(".")
        neg_name = "1" + "".join(data)
        pos_name = "2" + "".join(data)
        df = get_pandas(pango_path, 'WF_5', 'pangolin', ',')
        df = df.rename(columns=self.rename_po_cols_lst)

        # remove pooled samples from the run
        df = remove_pools(df, 'Sequence name')

        # remove any blanks from the run
        df = remove_blanks(df, 'Sequence name')

        # rename controls to appropriate format for database
        if self.include_controls:
            neg = False
            pos = False
            for index in range(len(df.index)):
                if "neg" in df['Sequence name'][index].lower():
                    neg_splt = df.at[index, 'Sequence name'].split("/")
                    neg_name = neg_name + "/" + "/".join(neg_splt[1:])
                    df.at[index, 'Sequence name'] = neg_name
                    neg = True
                if "pos" in df['Sequence name'][index].lower():
                    pos_splt = df.at[index, 'Sequence name'].split("/")
                    pos_name = pos_name + "/" + "/".join(pos_splt[1:])
                    df.at[index, 'Sequence name'] = pos_name
                    pos = True
                if neg and pos:
                    break

        # add columns
        df = add_cols(obj=self,
            df=df,
            col_lst=self.add_col_lst,
            col_func_map=self.col_func_map)
        df.rename(columns={"day_run_num_var":"day_run_num",
            "wgs_run_date_var":"wgs_run_date",
            "machine_num_var":"machine_num"}, inplace=True)
        
        # remove columns/split dataframes
        self.df_qc = df[self.full_lst]
        self.df_results = df[self.full_lst]
        self.log.write_log("get_pango_dfs","Completed")


    def database_push(self):
        self.log.write_log("database_push","Connecting to DB")
        super().setup_db()
        all_time_df_qc = self.db_handler.sub_read(query=self.read_query_tbl2)
        df_results_final = merge_dataframes(
            df1=all_time_df_qc,
            df2=self.df_results,
            df1_drop=['ID_Table_2', 'platform', 'percent_cvg', 'avg_depth',
            'total_ns', 'qc_snpclusters_status', 'qc_overall_status', 'path_to_fasta', 'position'],
            df_final_drop=['wgs_run_date', 'machine_num', 'position', 'day_run_num'],
            join_lst=["hsn", "wgs_run_date", "machine_num", "day_run_num"],
            join_type='left')

        df_results_final_lst = df_results_final.values.astype(str).tolist()
        self.log.write_log("database_push","Updating rows in the results table...")
        self.db_handler.lst_ptr_push(df_lst=df_results_final_lst, query=self.write_query_tbl1)
        self.log.write_log("database_push","Completed")



    def run_pangolin(self, path):
        self.log.write_log("run_pangolin","Starting")
        exec_cmd = "cd /home/ssh_user/pangolin-master/pangolin && source /home/ssh_user/miniconda3/bin/activate pangolin && pangolin " + path

        self.log.write_log("run_pangolin","Running the pangolin analysis, please wait...\n")
        # execute command
        run_obj = subprocess.run(exec_cmd, executable='/bin/bash', capture_output=True, shell=True)
        run_obj = subprocess.run("cp /home/ssh_user/pangolin-master/pangolin/lineage_report.csv "+"/".join(path.split('/')[:-1])+"/results.csv", shell=True)
        self.log.write_log("run_pangolin"," Pangolin analysis finished!")
