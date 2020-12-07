from threading import Thread
import time
from parseYaml import random_set_all_key, get_all_keys
from main import init_enviro
from getdataset import kill_vegeta, kill_docker_compose, nestedlist2csv
from run_vegeta import CURRENT_TRAFFIC, CURRENT_TRAFFIC_V2, init_docker, init_vegeta, init_vegeta_v2
from helper import get_throughput, get_mean_latency
import csv

# append new row to existing csv file
def appendlist2csv(one_record, out_file):
    with open(out_file, 'a') as f:
        w = csv.writer(f)
        w.writerow(one_record.values())

print("init docker")
Thread(target=init_docker).start()
time.sleep(25)

list_of_dict = []
for i in range(30):
    one_record = {}
    # set all key
    random_set_all_key()
    time.sleep(1)

    print("init vegeta")
    Thread(target=init_vegeta).start()
    Thread(target=init_vegeta_v2).start()

    time.sleep(20)
    print("kill vegeta")
    kill_vegeta(CURRENT_TRAFFIC)
    kill_vegeta(CURRENT_TRAFFIC_V2)

    time.sleep(1)
    r1_throughput = get_throughput('./out.txt')
    r2_throughput = get_throughput('./out2.txt')

    current_limit_dict = get_all_keys()
    for key, val in current_limit_dict.items():
        one_record[key] = val
    one_record["r1_throughput"] = r1_throughput
    one_record["r2_throughput"] = r2_throughput
    one_record["r1_mean_latency"] = get_mean_latency('./out.txt')
    one_record["r2_mean_latency"] = get_mean_latency('./out2.txt')
    one_record["throughput"] = r1_throughput + r2_throughput

    # list_of_dict.append(one_record)
    print("generate " + str(i)+ " th sample ..................")
    print(one_record)
    appendlist2csv(one_record, "checkerDatasetv2.csv")


# nestedlist2csv(list_of_dict, "checkerDataset" + time.asctime(time.localtime(time.time())) +".csv")
# nestedlist2csv(list_of_dict, "checkerDatasetv2.csv")

kill_docker_compose()
