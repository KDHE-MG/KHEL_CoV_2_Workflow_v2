from ..workflow_obj import workflow_obj
from ..reader import get_pandas
from ..ui import get_path
from ..formatter import add_cols, remove_blanks, remove_pools, merge_dataframes
from logger import Script_Logger
import subprocess

class WorkflowObj4(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_4"
        self.log = Script_Logger("WF_4_Parse_Nexcalde")
        self.log.start_log("Initalization of WF4")
    # methods
    def get_json(self):
        super().get_json(4)
        self.log.write_log("get_json","Argument Passed 4")

    def get_nextclade_dfs(self, nc_path=False):
        # open nextclade path --> pandas dataframe
        self.log.write_log("get_nextcalde_dfs","Starting function")
        if not nc_path:
            self.log.write_log("get_nextclade_dfs","Nextcalde Path Empty")
            print("\nUse the following window to open the nextclade results workbook...")
            nc_path = get_path()
        splt = nc_path.split("/")
        parent_folder = splt[-2]
        data = parent_folder.split(".")
        neg_name = "1" + "".join(data)
        pos_name = "2" + "".join(data)
        df = get_pandas(nc_path, "WF_4", "nextclade", '\t')
        df = df.rename(columns=self.rename_nc_cols_lst)
        
        # remove pooled samples from the run
        df = remove_pools(df, 'seqName')

        # remove any blanks from the run
        df = remove_blanks(df, 'seqName')

        # rename controls to appropriate format for database
        if self.include_controls:
            neg = False
            pos = False
            for index in range(len(df.index)):
                if "neg" in df['seqName'][index].lower():
                    neg_splt = df.at[index, 'seqName'].split("/")
                    neg_name = neg_name + "/" + "/".join(neg_splt[1:])
                    df.at[index, 'seqName'] = neg_name
                    neg = True
                if "pos" in df['seqName'][index].lower():
                    pos_splt = df.at[index, 'seqName'].split("/")
                    pos_name = pos_name + "/" + "/".join(pos_splt[1:])
                    df.at[index, 'seqName'] = pos_name
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

        df.fillna("", inplace=True)
        self.df_qc = df[self.nc_qc_cols_lst]
        self.df_results = df[self.nc_results_cols_lst]
        self.log.write_log("get_nextcalde_dfs","complete")

    def database_push(self):
        self.log.write_log("database_push","Attemping to connect to db")
        # attempt to connect to database
        super().setup_db()
        self.log.write_log("database_push","connect to db successful")
        df_qc_update_lst = self.df_qc.values.astype(str).tolist()
        self.log.write_log("database_push","Pushing information to Run Stats table")
        self.db_handler.lst_ptr_push(df_lst=df_qc_update_lst, query=self.write_query_tbl2)
        all_time_df_qc = self.db_handler.sub_read(query=self.read_query_tbl2)
        
        df_results_final = merge_dataframes(\
            df1=all_time_df_qc, \
            df2=self.df_results, \
            df1_drop=['ID_Table_2', 'percent_cvg', 'avg_depth', 'total_ns'], \
            df_final_drop=['wgs_run_date', 'machine_num', 'position', 'day_run_num'], \
            join_lst=["hsn", "wgs_run_date", "machine_num", "position", "day_run_num"], \
            join_type='inner')

        df_results_final_lst = df_results_final.values.astype(str).tolist()
        if len(df_results_final_lst) == 0:
            self.log.write_warning("database_push","Nextclade data from this run has likely already been pushed to the database!")
            raise ValueError("\n-------------------------------------------------------------------------------------------------------------------\
                \nNextclade data from this run has likely already been pushed to the database!\
                \n-------------------------------------------------------------------------------------------------------------------")
        self.log.write_log("database_push","Updating rows in the results table")
        self.db_handler.lst_ptr_push(df_lst=df_results_final_lst, query=self.write_query_tbl1)
        self.log.write_log("database_push","Completed")


    def run_nextclade(self, path):
        self.log.write_log("run_nextclade","starting")
        # connection to the server has already been established
        # check for updates and update if needed
        exec_cmd = "cd nextclade-master && ./nextclade --in-order --input-fasta=" + path + \
" --input-dataset=data/sars-cov-2 --output-tsv=output/nextclade.tsv --output-dir=output/ --output-basename=nextclade"

        self.log.write_log("run_nextclade","Attempting to run the Nextclade application, please wait.\n")
        # execute command
        run_obj = subprocess.run(exec_cmd, capture_output=True, shell=True)
        print(run_obj.stderr.decode())
        print(run_obj.stdout.decode())
        self.log.write_log("run_nextclade"," Nextclade analysis finished!")

