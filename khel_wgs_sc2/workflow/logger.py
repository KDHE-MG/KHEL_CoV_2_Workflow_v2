#import libs
import logging

logger_file_path=""

class Script_Logger() :

    def __init__(self,function_name) -> None:
        self = logger.getLogger(function_name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        file_handler = logging.FileHandler(logger_file_path+"/"+function_name+".log")
        file_hanlder.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        

    def write_log (self,s_command=None, info=None ):
        self.logger.INFO("Function "+s_command+" was called")

