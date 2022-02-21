import sys
import time
import subprocess

if __name__ == "__main__":
    # TODO
    #run_id = str(sys.argv[1])
    run_id = "BB1L12.2022-02-18.01"
    print("\nSpinning up scripts, please wait...\n")

    try:
        subprocess.run("./khel_wgs_sc2/khel_wgs_sc2.py " + run_id, shell=True)
    except Exception as e:
        print(e)
        time.sleep(20)
    print("\nExiting caller script")
    time.sleep(1)


    print("run id: " + str(run_id))