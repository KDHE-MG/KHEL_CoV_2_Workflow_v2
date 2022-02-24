#import libs
import logging



class Script_Logger() :

    def __init__(self,function_name) -> None:
        self.logger = logging.getLogger(function_name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        file_handler = logging.FileHandler("/data/log_files/"+function_name+".log")

        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
    
    def start_log(self, description):
        self.logger.DEBUG(description)

    def write_log (self,s_command=None, info=None ):
        self.logger.INFO("Function "+s_command+" was called with this description"+info)
    
    def write_warning(self,s_command="",issue=""):
        self.logger.warning("Function "+s_command+ "had this issue "+issue)
