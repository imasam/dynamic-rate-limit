from helper import generate_dataet, get_mean_latency
from parseYaml import get_all_keys, get_key, edit_key
from run_vegeta import get_current_limit, CURRENT_TRAFFIC, CURRENT_TRAFFIC_V2
from subprocess import Popen
import random
import csv
import logging
import subprocess
import sys
import pandas as pd
import argparse
import os
from config import CURRENT_REQUEST_SERVICE, query_dict


PERCENT = 0.1
NUMOFRECORD = 1
DOCKER_YAML = "../envoy_monitoring/docker-compose.yml"
CURRENT_REQUEST_SERVICE = CURRENT_REQUEST_SERVICE

current_limit_str = str(get_current_limit(CURRENT_REQUEST_SERVICE))
current_limit = int(current_limit_str)

# get vegeta's pid
def getPid(process):
    cmd = "ps aux | grep '%s' " % process
    logging.info(cmd)
    info = subprocess.getoutput(cmd)
    infos = info.split()
    if len(infos) > 1:
        print(infos[1])
        return infos[1]
    else:
        return -1

def kill_vegeta(traffic):
    vegeta_pid = getPid("vegeta attack -rate=" + traffic)
    command = "kill -9 " + str(vegeta_pid)
    print(command)
    subprocess.call(command, shell=True)
    print("kill vegeta success")

def kill_docker_compose():
    command = "docker-compose -f " + DOCKER_YAML + " stop"
    print(command)
    subprocess.call(command, shell=True)
    print("kill docker-compose success")

def nestedlist2csv(list, out_file):
    with open(out_file, 'w') as f:
        w = csv.writer(f)
        fieldnames=list[0].keys()  # solve the problem to automatically write the header
        w.writerow(fieldnames)
        for row in list:
            w.writerow(row.values())


def appendLatency(sourceFile, outputFile, latency):
    sourceFile = sourceFile
    df = pd.read_csv(sourceFile,low_memory=False) 
    df['mean_latency'] = latency 
    print("append latency success!!")

    columns_val = list(df.columns.values)

    df.to_csv(outputFile, columns=columns_val, index=0, header=1)


if __name__ == "__main__":
    # generate dataset
    list_of_dict = generate_dataet(NUMOFRECORD, query_dict)

    nestedlist2csv(list_of_dict, CURRENT_REQUEST_SERVICE + "_" + current_limit_str + ".csv")

    print("kill vegeta and stop docker compose")
    kill_vegeta(CURRENT_TRAFFIC)
    kill_vegeta(CURRENT_TRAFFIC_V2)

    kill_docker_compose()

    latency = get_mean_latency("./out.txt")
    sourceFile = CURRENT_REQUEST_SERVICE + "_" + current_limit_str + ".csv"
    outputFile = sourceFile

    appendLatency(sourceFile, outputFile, latency)
