import subprocess
from threading import Thread
import time
from parseYaml import random_set_all_except_one, edit_key
from config import CURRENT_REQUEST_SERVICE
import argparse

def init_enviro():
    command = "python3 run_vegeta.py"
    subprocess.call(command, shell=True)

def start_collect():
    command = "python3 getdataset.py"
    subprocess.call(command, shell=True)

def start_random_setlimit(t1):
    while t1.isAlive():
        random_set_all_except_one(CURRENT_REQUEST_SERVICE)
        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description='args parser'
    parser.add_argument("limit",type=int)
    args = parser.parse_args()
    # comment when using automate
    edit_key(CURRENT_REQUEST_SERVICE, args.limit)
    # exit()

    Thread(target=init_enviro).start()
    time.sleep(30)

    t1 = Thread(target=start_collect)
    t1.start()
    # random set other's limit
    Thread(target=start_random_setlimit, args=(t1,)).start()
