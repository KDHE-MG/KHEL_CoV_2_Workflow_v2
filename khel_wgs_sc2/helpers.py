from workflow.WF_0_scrape_web.WF_0_scrape_web import run_script_0
from workflow.WF_0_5_extract.WF_0_5_extract import run_script_0_5
from workflow.WF_1_import_demos.WF_1_import_demos import run_script_1
from workflow.WF_2_parse_run_data.WF_2_parse_run_data import run_script_2
from workflow.WF_3_compile_fasta.WF_3_compile_fasta import run_script_3
from workflow.WF_4_parse_nextclade.WF_4_parse_nextclade import run_script_4
from workflow.WF_5_parse_pangolin.WF_5_parse_pangolin import run_script_5
from workflow.WF_6_build_epi_report.WF_6_build_epi_report import run_script_6
from workflow.WF_7_send_epi_report.WF_7_send_epi_report import run_script_7
from workflow.WF_8_sync_network.WF_8_sync_network import run_script_8
from workflow.WF_9_send_fastas.WF_9_send_fastas import run_script_9
from workflow.epi_isl.epi_isl import run_epi_isl
from workflow.gisaid.gisaid import run_gisaid
from workflow.outside_lab.outside_lab import run_outside_lab
from workflow.gisaid_submit.gisaid_submit import run_gisaid_submit
# TODO bokeh import not working
#from workflow.plotter.plotter import run_plotter
import pyodbc
import time
import threading
import datetime
import os


def run_set_1(run_id):
    # run_script_1 will read in all hsn's from run_data.json file and fetch patient demographics
    # from oracle database, clean the data, and push it to the SQL database
    run_script_1(run_id)

    # run_script_2 will read in all run_stats from run_data.json file, and push the data to the
    # SQL database.  Requires run_script_1 to run first
    run_script_2(run_id) #needs run to open json and open run info


def run_set_2(run_id):
    # run_script_0_5 will extract fasta files downloaded in WF_0
    run_script_0_5(run_id)

    # run_script_3 will take all the FASTA files and combine them into one
    run_script_3(run_id)


def run(run_id):
    print("\n ___________________________________________________\n|  _______________________________________________  |\n| |\033[4m    SARS-CoV-2 daily workflow runner script    \033[0m| |\n|___________________________________________________|\n")
    ask = True

    

    if run_id != "windows":
        try:
            # run_script_0 will perform web-scraping and save information in run_data.json file
            # run_script_0 will also download the FASTA/Q files for use later.  It MUST finish execution
            # before anything else starts
            #lock_file = open("/home/ssh_user/WGS_Sequencing_COVID/lock_file.txt", "w")
            #run_script_0(run_id)

            run_script_0_5(run_id)
            run_script_1(run_id)
            run_script_2(run_id)
            run_script_3(run_id)
            run_script_4(run_id)
            run_script_5(run_id)
            run_script_6(run_id)
            run_gisaid(run_id)
            #run_gisaid_submit(run_id)

           
            # TODO setup thread pooling to reduce resource
            # requirements

            # t1 = threading.Thread(target=run_set_1, args=run_id)
            # t2 = threading.Thread(target=run_set_2, args=run_id)

            # # start multitasking
            # t1.start() # WF 1, 2
            # t2.start() # WF 0_5, 3

            # # WF 2 and 3 must finish before 4 and 5 start
            # t1.join()
            # t2.join()
            
            # # TODO - access fasta path within run_script 4 and 5 via run_id
            # t3 = threading.Thread(target=run_script_4, args=run_id)
            # t4 = threading.Thread(target=run_script_5, args=run_id)
            # t3.start()
            # t4.start()
            # t3.join()
            # t4.join()
            
            # run_date = datetime.datetime.strptime(run_id[7:17], '%Y-%m-%d').strftime("%m/%d/%Y")
            # run_script_9(run_date)
            #run_gisaid()
            
            # t5 = threading.Thread(target=run_script_9, args=run_date)
            #t6 = threading.Thread(target=run_gisaid)

            # we can have the script grab all 64 samples for the day
            # since it will just create 2 files, one for each run
            # t7 = threading.Thread(target=run_script_6, args=run_id)
            # t5.start()

            # t6.start()
            # t7.start()
            # t5.join()
            # t6.join()
            # t7.join()

            # release the results
            lock_file.close()
            os.remove("/home/ssh_user/WGS_Sequencing_COVID/lock_file.txt")

        except pyodbc.IntegrityError as i:
            print(i)
            print("\nThis usually happens when the run data has already been imported into the database")
            lock_file.close()
            os.remove("/home/ssh_user/WGS_Sequencing_COVID/lock_file.txt")
            time.sleep(5)
        except Exception as i:
            print(i)
            lock_file.close()
            os.remove("/home/ssh_user/WGS_Sequencing_COVID/lock_file.txt")
            time.sleep(5)

    else:
        # script is being called by a user on windows
        while ask:
            u_input = input("\n\nenter '6' to build an epi report\nenter '7' to send an epi report\nenter '8' to pull all results files from Linux\
                \n\nOther options:\
                \nenter 'plotter' to get an interactive dashboard of the database\
                \nenter 'outside lab' to import a data template submitted from an outside lab\
                \nenter 'epi isl' to update all isl numbers for samples submitted to gisaid\n\nenter 'q' to quit\n--> ")
            try:
                    
                if u_input.strip().lower() == '6':
                    run_script_6(run_id)
                    
                elif u_input.strip().lower() == '7':
                    run_script_7()

                elif u_input.strip().lower() == '8':
                    run_script_8()
                    
                elif u_input.strip().lower() == 'outside lab':
                    # run script
                    run_outside_lab()
                
                elif u_input.strip().lower() == 'epi isl':
                    # run script
                    run_epi_isl()
                    
                elif u_input.strip().lower() == 'q':
                    ask = False
                
                else:
                    raise ValueError("Invalid input!")

            except Exception as i:
                print(i, str(type(i)))
                time.sleep(2)
            
            