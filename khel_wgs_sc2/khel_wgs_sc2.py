import sys
import time
from helpers import run

if __name__ == "__main__":
    try:
<<<<<<< HEAD
        if len(sys.argv) == 1:
            run_id = "windows"
        else:
            run_id = str(sys.argv[1])
            # call to main script
=======
        run_id = sys.argv[1:]
        # call to main script
>>>>>>> 6500aa90c9aea3ded7cad09b7dcfc39d2648d61b
        run(run_id)
    except Exception as e:
        print(e)
        time.sleep(500)

