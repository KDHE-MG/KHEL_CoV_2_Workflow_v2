import sys

if __name__ == "__main__":
    run_id = sys.argv[1]
    import time

    f = open('testfile.txt', 'a')
    f.write(run_id)
    f.close()
    
    print("Hello World!")
    print("The other stuff!")
    time.sleep(5)
    print("The final stuff")
    print("run id: " + str(run_id))