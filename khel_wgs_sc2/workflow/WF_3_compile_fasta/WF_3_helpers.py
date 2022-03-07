from ..workflow_obj import workflow_obj
from ..formatter import add_cols, remove_pools, remove_blanks
import os
import pandas as pd
import datetime
from workflow.logger import Script_Logger


class WorkflowObj3(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "WF_3"
        self.log = Script_Logger("WF_3_Compile_Fasta")
        self.log.start_log("Initalization of WF3")
    
    # methods
    def get_json(self):
        super().get_json(3)
        self.log.write_log("get_json","Argument passed 3")

    def compile_fasta(self, run_id):
        self.log.write_log("compile_fasta","Starting")
        #print("Use the following dialog box to select the folder with all FASTA files in the Run Data folder")
        
        # the path to the file will be dependent on the run_id,
        # and constant otherwise.  get_path_folder and replace_shortcut
        # not needed

        machine_num = run_id[4:6]
        run_date = datetime.datetime.strptime(run_id[7:17], '%Y-%m-%d').strftime("%m%d%y")
        day_run_num = str(int(run_id[-2:]))

        run_id  = run_date + "." + machine_num + "." + day_run_num


        self.path =  self.fasta_file_path + run_id + "/FAST files"

        # make new folder/file to save to
        splt = self.path.split("/")
        if splt[-1] != "FAST files":
            self.log.write_warning("complie_fasta","No Fasta Files Folder found")
            raise ValueError("\n-------------------------------------------------------------------------------------------------------------------\
                \nThe selected folder is unexpected!  Select a folder with the name 'FAST files'\
                \n-------------------------------------------------------------------------------------------------------------------")
        folder_name = splt[-2]
        date = datetime.datetime.strptime(folder_name.split(".")[0], "%m%d%y").strftime("%m%d%y")
        machinenum = folder_name[-4:-2]
        filename = "all_" + date + "_" + machinenum + ".fasta"

        # make file to save to
        #if splt[-3] == "ClearLabs" or splt[-3] == "ClearLabs downloads":
        path_write = "/".join(splt[:-1]) + "/" + filename
    
        extension = ".fasta"
        
        # initialize string that will hold all the sequence data
        # and write to file f
        self.seqName_lst = []
        s = ""
        ctr = 0
        self.log.write_log("complie_fasta","begining to complie fasta")
        f = open(path_write, "w")
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(extension):
                    curr_file = open(self.path + "/" + file, "r")
                    file_contents = curr_file.readlines()
                    curr_file.close()
                    s += ""
                    for line in file_contents:
                        s += line
                    f.write(s)
                    s = ""
                    print("finished with file ", ctr)
                    ctr += 1
                    self.seqName_lst.append(file)
        f.close()
        if self.analysis_pathway == "cli":
            return path_write
        else:
            return ""

    def get_fasta_path_df(self):
        self.log.write_log("get_fasta_path_df","Starting")
        # transform dictionary of hsn/path into dataframe
        self.df = pd.DataFrame(self.seqName_lst, columns=['seqName'])
        # remove pooled samples from dataframe
        self.df = remove_pools(self.df, 'seqName')
        
        # remove any blanks from the run
        self.df = remove_blanks(self.df, 'seqName')
        self.log.write_log("get_fasta_path_df","droping controls")
        #drop controls from index
        if self.include_controls:
            neg = False
            pos = False
            to_drop = []
            for index in range(len(self.df.index)):
                if "neg" in self.df['seqName'][index].lower():
                    #neg_idx = index
                    to_drop.append(index)
                    neg = True

                if "pos" in self.df['seqName'][index].lower():
                    #pos_idx = index
                    to_drop.append(index)
                    pos = True
                if neg and pos:
                    break
            #self.df.drop([pos_idx, neg_idx], inplace=True)
            self.df.drop(to_drop, inplace=True)
        self.log.write_log("get_fasta_path","adding columns")
        # add columns
        add_cols(obj=self, \
            df=self.df, \
            col_lst=self.add_col_lst, \
            col_func_map=self.col_func_map)
        self.df.drop(labels=['seqName'], axis=1, inplace=True)
        self.df.rename(columns={"day_run_num_var":"day_run_num", \
            "wgs_run_date_var":"wgs_run_date"}, inplace=True)


    def database_push(self):
        self.log.write_log("database_push","connecting to db")
        # attempt to connect to database
        super().setup_db()
        df_lst = self.df.values.astype(str).tolist()
        #print("pushing to run_stats")
        #print(df_lst)
        self.db_handler.lst_ptr_push(df_lst=df_lst, query=self.write_query_tbl2)

    def delete_compress_fasta(self, runID):
        if os.path.exists(self.fasta_file_path+"/"+runID+"/"+runID+".all.tar.gz"):
            os.remove(self.fasta_file_path+"/"+runID+"/"+runID+".all.tar.gz")
            
        else:
            self.log.write_warning("No Compressed Fasta File found")

