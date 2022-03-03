import time
import datetime
from tkinter import filedialog 
from tkinter import *
import re
from turtle import position
import json
import os


def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = u"\u2588", printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def get_run_data(runID_ui):
    # get seq run id next
    platform = "ClearLabs"
    seq_run_id = runID_ui
    # ask = True
    # while ask:
    #     seq_run_id = input("\nPlease copy/paste the seq_run_id value from the ClearLabs website below\nExample: Run BB1L12.2021-06-16.01\n--> ")
        
    #     # check that input is valid
    #     if not re.search("Run BB\dL\d{2}.\d{4}-\d{2}-\d{2}.\d{2}", seq_run_id):
    #         print("Invalid input, try again.")
    #     else:
    #         ask = False
    
    # now, pull meaningful information out of supplied data
    machine_num = seq_run_id[4:6]
    run_date = datetime.datetime.strptime(seq_run_id[7:17], '%Y-%m-%d').strftime("%m/%d/%Y")
    day_run_num = int(seq_run_id[-2:])

    # get the run data from clearlabs21
    #ask = True
    #print("\nPlease copy/paste all run data from the clearlabs website below\n")
    #c = 0
    #pos_dict = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8}
    
    run_data = {"hsn":[], "position":[], "avg_depth":[], "percent_cvg":[]}

    script_dir = "/".join(os.path.abspath(__file__).split('/')[:-3])
    rel_path = "/data/run_data.json"
    abs_path = script_dir + rel_path

    file = open(abs_path, "r")
    run_dump = json.load(file)
    file.close()

    for hsn in [*run_dump[runID_ui]]:
        run_data["hsn"].append(hsn)
        run_data["position"].append(run_dump[runID_ui][hsn][0])
        run_data["avg_depth"].append(int(run_dump[runID_ui][hsn][3][:-1]))
        run_data["percent_cvg"].append(float(run_dump[runID_ui][hsn][4][:-1])/100)
    
    return run_data, machine_num, run_date, day_run_num, platform ;


def get_path():
    time.sleep(1)
    print("Opening dialog box...")
    time.sleep(1)
    root = Tk()
    root.withdraw()
    path_read = filedialog.askopenfilename()
    return path_read


def get_path_folder():
    time.sleep(1)
    print("Opening dialog box...")
    time.sleep(1)
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    return path

