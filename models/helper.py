import requests
import json
import time
import re
from queue import Queue
from threading import Thread
from parseYaml import get_all_keys, get_key, edit_key
from run_vegeta import get_current_limit
import subprocess
import logging
import random 
from config import CURRENT_REQUEST_SERVICE,query_dict

PERCENT = 0.1
CURRENT_TRAFFIC = "98"
CURRENT_TRAFFIC_V2 = "99"
TIME_TO_SLEEP = 4
current_limit_str = str(get_current_limit(CURRENT_REQUEST_SERVICE))
current_limit = int(current_limit_str)

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

def init_vegeta():
    command = "echo GET \"http://localhost:10000/request1\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC + " -duration=0 | vegeta report > out3.txt"
    subprocess.call(command, shell=True)

def init_vegeta_v2():
    command = "echo GET \"http://localhost:10000/request2\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC_V2 + " -duration=0 | vegeta report > out4.txt"
    subprocess.call(command, shell=True)

def get_throughput(file_path):
    
    f = open(file_path)
    line = f.readline()
    lines = []
    while line:
        lines.append(line)
        line = f.readline()
    sub1 = re.sub('Success', ' ', lines[5])
    latency = re.sub('\[ratio\]', ' ', sub1)
    latency = float(latency.lstrip().rstrip()[:-1])
    f.close()
    # print(latency)
    return latency


def get_throughput_from_vegeta():
    Thread(target=init_vegeta).start()
    Thread(target=init_vegeta_v2).start()

    time.sleep(10)
    print("kill vegeta")
    kill_vegeta(CURRENT_TRAFFIC)
    kill_vegeta(CURRENT_TRAFFIC_V2)

    time.sleep(10)
    r1_throughput = get_throughput('./out3.txt')
    r2_throughput = get_throughput('./out4.txt')
    current_overall_throughput = r1_throughput + r2_throughput

    return current_overall_throughput

def add_next_new_limit(one_dict):
    up_size = random.randint(int(current_limit * (1+(PERCENT/2))), int(current_limit * (1+PERCENT)))
    down_size = random.randint(int(current_limit * (1-PERCENT)), int(current_limit * (1-(PERCENT/2))))

    res_list = []
    res_list.append([get_throughput_from_vegeta(), current_limit])

    edit_key(CURRENT_REQUEST_SERVICE, up_size)
    time.sleep(2)
    res_list.append([get_throughput_from_vegeta(), up_size])

    edit_key(CURRENT_REQUEST_SERVICE, down_size)
    time.sleep(2)
    res_list.append([get_throughput_from_vegeta(), down_size])

    one_dict["new_limit"] = max(res_list)[1]
    print("in add next new limit")
    print(one_dict)



def wrapper(func, queue, query_target):
       queue.put(func(query_target))

def rq_pending_total(query_target):
    url = "http://localhost:9090/api/v1/query?query=" + query_target
    # url = "http://localhost:9090/api/v1/query?query=service_a_cluster_service_a_upstream_rq_pending_total"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    response_json = json.loads(response.text)
    res = 0
    if 'data' in response_json.keys():
        res = int(response_json['data']['result'][0]['value'][1])
    
    # print("rq_pending_total ", res)
    return res

# [1, 2, 3]
def rq_time(query_target):
    url = "http://localhost:9090/api/v1/query?query=" + query_target
    # url = "http://localhost:9090/api/v1/query?query=service_a_cluster_service_a_upstream_rq_time"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    
    res = []
    for i in range(len(response_json['data']['result'])):
        res.append(response_json['data']['result'][i]['value'][1])

    # print("rq_time ", res)
    return res

def upstream_rq_total(query_target):
    url = "http://localhost:9090/api/v1/query?query=" + query_target
    # url = "http://localhost:9090/api/v1/query?query=service_a_cluster_service_a_upstream_rq_total"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text)

    res = 0
    res = int(response_json['data']['result'][0]['value'][1])

    # print("upstream_rq_total ", res)
    return res

def upstream_rq_completed(query_target):
    url = "http://localhost:9090/api/v1/query?query=" + query_target
    # url = "http://localhost:9090/api/v1/query?query=service_a_cluster_service_a_upstream_rq_completed"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    
    res = 0
    res = int(response_json['data']['result'][0]['value'][1])
    # print("upstream_rq_completed ", res)
    return res

def rq_active(query_target):
    url = "http://localhost:9090/api/v1/query?query=" + query_target
    # url = "http://localhost:9090/api/v1/query?query=service_a_cluster_service_a_upstream_rq_active"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    
    res = 0
    res = int(response_json['data']['result'][0]['value'][1])
    # print("rq_active ", res)
    return res

# rq_active()

def generate_dataet(NUM_OF_RECORD, query_dict):
    list_of_dict = []
    for i in range(NUM_OF_RECORD):
        one_record = {}
        upstream_rq_total_val = upstream_rq_total(query_dict['rq_total'])
        # rq_time_val = rq_time()
        # pending_rate = int(rq_pending_total() / upstream_rq_total_val)
        # complete_rate = int(upstream_rq_completed() / upstream_rq_total_val)
        # active_rate = int(rq_active() / upstream_rq_total_val)
        q1, q2, q3, q4, q5, q6 = Queue(), Queue(), Queue(), Queue(), Queue(), Queue()

        Thread(target=wrapper, args=(rq_time, q1, query_dict['service_a_rq_time'])).start()
        Thread(target=wrapper, args=(rq_pending_total, q2, query_dict['rq_pending_total'])).start()
        Thread(target=wrapper, args=(upstream_rq_completed, q3, query_dict['rq_completed'])).start()
        Thread(target=wrapper, args=(rq_active, q4, query_dict['rq_active'])).start()
        Thread(target=wrapper, args=(rq_time, q5, query_dict['service_b_rq_time'])).start()
        Thread(target=wrapper, args=(rq_time, q6, query_dict['service_c_rq_time'])).start()
        

        rq_time_val = q1.get()
        pending_rate = q2.get() / upstream_rq_total_val
        complete_rate = q3.get() / upstream_rq_total_val
        active_rate = q4.get() / upstream_rq_total_val
        current_limit_dict = get_all_keys()

        rq_time_val_vb = q5.get()
        rq_time_val_vc = q6.get()

        # one_record["upstream_rq_total"] = upstream_rq_total_val
        one_record["service_a_rq_time_50_quantile"] = rq_time_val[0]
        one_record["service_a_rq_time_90_quantile"] = rq_time_val[1]
        one_record["service_a_rq_time_99_quantile"] = rq_time_val[2]

        one_record["service_b_rq_time_50_quantile"] = rq_time_val_vb[0]
        one_record["service_b_rq_time_90_quantile"] = rq_time_val_vb[1]
        one_record["service_b_rq_time_99_quantile"] = rq_time_val_vb[2]

        one_record["service_c_rq_time_50_quantile"] = rq_time_val_vc[0]
        one_record["service_c_rq_time_90_quantile"] = rq_time_val_vc[1]
        one_record["service_c_rq_time_99_quantile"] = rq_time_val_vc[2]

        one_record["pending_rate"] = pending_rate
        one_record["complete_rate"] = complete_rate
        one_record["active_rate"] = active_rate
        
        for key, val in current_limit_dict.items():
            one_record[key] = val

        print("try to add new next limit")
        add_next_new_limit(one_record)

        list_of_dict.append(one_record)
        print("generate " + str(i)+ " th sample ..................")
        print(one_record)
        # sleep for a while
        time.sleep(TIME_TO_SLEEP)
    

    # print(list_of_dict)
    return list_of_dict

def generate_metric(NUM_OF_RECORD, query_dict):
    list_of_dict = []
    for i in range(NUM_OF_RECORD):
        one_record = {}
        upstream_rq_total_val = upstream_rq_total(query_dict['rq_total'])
        # rq_time_val = rq_time()
        # pending_rate = int(rq_pending_total() / upstream_rq_total_val)
        # complete_rate = int(upstream_rq_completed() / upstream_rq_total_val)
        # active_rate = int(rq_active() / upstream_rq_total_val)
        q1, q2, q3, q4, q5, q6 = Queue(), Queue(), Queue(), Queue(), Queue(), Queue()

        Thread(target=wrapper, args=(rq_time, q1, query_dict['service_a_rq_time'])).start()
        Thread(target=wrapper, args=(rq_pending_total, q2, query_dict['rq_pending_total'])).start()
        Thread(target=wrapper, args=(upstream_rq_completed, q3, query_dict['rq_completed'])).start()
        Thread(target=wrapper, args=(rq_active, q4, query_dict['rq_active'])).start()
        Thread(target=wrapper, args=(rq_time, q5, query_dict['service_b_rq_time'])).start()
        Thread(target=wrapper, args=(rq_time, q6, query_dict['service_c_rq_time'])).start()
        

        rq_time_val = q1.get()
        pending_rate = q2.get() / upstream_rq_total_val
        complete_rate = q3.get() / upstream_rq_total_val
        active_rate = q4.get() / upstream_rq_total_val
        current_limit_dict = get_all_keys()

        rq_time_val_vb = q5.get()
        rq_time_val_vc = q6.get()

        # one_record["upstream_rq_total"] = upstream_rq_total_val
        one_record["service_a_rq_time_50_quantile"] = rq_time_val[0]
        one_record["service_a_rq_time_90_quantile"] = rq_time_val[1]
        one_record["service_a_rq_time_99_quantile"] = rq_time_val[2]

        one_record["service_b_rq_time_50_quantile"] = rq_time_val_vb[0]
        one_record["service_b_rq_time_90_quantile"] = rq_time_val_vb[1]
        one_record["service_b_rq_time_99_quantile"] = rq_time_val_vb[2]

        one_record["service_c_rq_time_50_quantile"] = rq_time_val_vc[0]
        one_record["service_c_rq_time_90_quantile"] = rq_time_val_vc[1]
        one_record["service_c_rq_time_99_quantile"] = rq_time_val_vc[2]

        one_record["pending_rate"] = pending_rate
        one_record["complete_rate"] = complete_rate
        one_record["active_rate"] = active_rate
        
        for key, val in current_limit_dict.items():
            one_record[key] = val

        list_of_dict.append(one_record)
        # print("generate " + str(i)+ " th sample ..................")
        # print(one_record)
        # sleep for a while
        time.sleep(TIME_TO_SLEEP)
    

    # print(list_of_dict)
    return list_of_dict

def get_mean_latency(file_path):
    
    f = open(file_path)
    line = f.readline()
    lines = []
    while line:
        lines.append(line)
        line = f.readline()
    latency = re.sub(' +', ' ', lines[2]).split(' ')[9][:-3]
    f.close()
    latency = float(latency) / 1000
    # print("latency ", latency)
    return latency


# get_throughput("./out.txt")
# get_throughput_from_vegeta()
# generate_dataet(1, query_dict)
