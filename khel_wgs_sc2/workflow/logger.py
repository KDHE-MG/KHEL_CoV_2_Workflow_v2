#import libs
import logging

from pathlib import Path
import os



class Script_Logger() :

    def __init__(self,function_name) -> None:
        
        #logging.basicConfig(filemode='w+')
        self.logger = logging.getLogger(function_name)
        self.logger.setLevel(logging.DEBUG)
        
        

        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        script_dir = "/".join(os.path.abspath(__file__).split('/')[:-3])
        rel_path = "/data/log_files/"+function_name+".log"
        abs_path = script_dir + rel_path
        Path(abs_path).touch(exist_ok=True)
        
        file_handler = logging.FileHandler(abs_path, mode ='w')
       

        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
     
     
    
    def start_log(self, description):
        self.logger.debug(description)

    def write_log (self,s_command="", info="" ):
        self.logger.info("Function "+s_command+" was called with this description:\n-->"+info)
    
    def write_warning(self,s_command="",issue=""):
        self.logger.warning("Function "+s_command+ " had this issue:\n-->"+issue)
