from workflow.WF_0_scrape_web.WF_0_scrape_web import run_script_0
from workflow.WF_1_import_demos.WF_1_import_demos import run_script_1
from workflow.WF_2_parse_run_data.WF_2_parse_run_data import run_script_2
from workflow.WF_3_compile_fasta.WF_3_compile_fasta import run_script_3
from workflow.WF_4_parse_nextclade.WF_4_parse_nextclade import run_script_4
from workflow.WF_5_parse_pangolin.WF_5_parse_pangolin import run_script_5
from workflow.WF_6_build_epi_report.WF_6_build_epi_report import run_script_6
from workflow.WF_7_send_epi_report.WF_7_send_epi_report import run_script_7
from workflow.WF_9_send_fastas.WF_9_send_fastas import run_script_9
from workflow.epi_isl.epi_isl import run_epi_isl
from workflow.gisaid.gisaid import run_gisaid
from workflow.outside_lab.outside_lab import run_outside_lab
from workflow.plotter.plotter import run_plotter
import pyodbc
import time
import threading

def run_set_2():
    # run_script_2 will read in all run_stats from run_data.json file, and push the data to the
    # SQL database.  Requires run_script_1 to run first
    # TODO store day in json file within script 2?
    run_script_2()

    # run_script_3 will take all the FASTA files and combine them into one
    run_script_3()


def run(run_id="windows"):
    print("\n ___________________________________________________\n|  _______________________________________________  |\n| |\033[4m    SARS-CoV-2 daily workflow runner script    \033[0m| |\n|___________________________________________________|\n")
    
    ask = True

    

    if run_id != "windows":
        try:
            # run_script_0 will perform web-scraping and save information in run_data.json file
            # run_script_0 will also download the FASTA/Q files for use later.  It MUST finish execution
            # before anything else starts
            # TODO
            run_script_0(run_id)

            # run_script_1 will read in all hsn's from run_data.json file and fetch patient demographics
            # from oracle database, clean the data, and push it to the SQL database
            t1 = threading.Thread(target=run_script_1)
            t2 = threading.Thread(target=run_set_2, args=run_id)

            # start multitasking
            t1.start() # WF 1
            t2.start() # WF 2, 3
            # WF 2 and 3 must finish before 4 and 5 start
            t2.join()
            
            # TODO - access fasta path within run_script 4 and 5 via run_id
            t3 = threading.Thread(target=run_script_4, args=run_id)
            t4 = threading.Thread(target=run_script_5, args=run_id)
            t3.start()
            t4.start()
            t3.join()
            t4.join()
            
            t5 = threading.Thread(target=run_script_9, args=run_id)
            t6 = threading.Thread(target=run_gisaid)

            # TODO this query functions differently and only should retrieve
            # the epi report for the 32 samples just analyzed.  Not the whole
            # 64 samples for the day
            t7 = threading.Thread(target=run_script_6, args=run_id)
            t5.start()

            # need patient demographics before running gisaid
            # and epi report scripts
            t1.join()

            t6.start()
            t7.start()
            t5.join()
            t6.join()
            t7.join()

        except pyodbc.IntegrityError as i:
            print(i)
            print("\nThis usually happens when the run data has already been imported into the database")
            time.sleep(5)
        except Exception as i:
            print(i)
            time.sleep(5)

    else:
        # script is being called by a user on windows
        while ask:
            u_input = input("\n\nenter '6' to build an epi report\nenter '7' to send an epi report\
                \n\nOther options:\
                \nenter 'plotter' to get an interactive dashboard of the database\
                \nenter 'outside lab' to import a data template submitted from an outside lab\
                \nenter 'epi isl' to update all isl numbers for samples submitted to gisaid\n\nenter 'q' to quit\n--> ")
            try:
                    
                if u_input.strip().lower() == '6':
                    run_script_6()
                    
                elif u_input.strip().lower() == '7':
                    run_script_7()

                elif u_input.strip().lower() == 'plotter':
                    # run script
                    run_plotter()
                    
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
            
            