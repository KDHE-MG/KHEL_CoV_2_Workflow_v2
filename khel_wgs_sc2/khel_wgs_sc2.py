import sys
import time
from helpers import run

if __name__ == "__main__":
    # try:
    #     if len(sys.argv) == 1:
    #         run_id = "windows"
    #     else:
    #         run_id = str(sys.argv[1])
    #         # call to main script
    #     run(run_id)
    # except Exception as e:
    #     print(e)
    #     time.sleep(500)
    try:
        run_id = "BB1L13.2022-02-28.01"
        run(run_id)
    except Exception as e:
        print(e)
        time.sleep(400)

