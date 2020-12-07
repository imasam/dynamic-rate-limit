from helper import generate_metric, get_throughput, get_mean_latency
from parseYaml import get_all_keys, edit_key, get_key
from threading import Thread
from getdataset import kill_vegeta
import time
import subprocess
from model import checkerInfer, r1_b_predictor, r2_b_predictor, fc_model

CURRENT_TRAFFIC = "102"
CURRENT_TRAFFIC_V2 = "112"
R1_PRIORITY = 1
R2_PRIORITY = 2


def init_vegeta():
    command = "echo GET \"http://localhost:10000/request1\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC + " -duration=0 | vegeta report > servicecb.txt"
    subprocess.call(command, shell=True)

def init_vegeta_v2():
    command = "echo GET \"http://localhost:10000/request2\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC_V2 + " -duration=0 | vegeta report > servicecb2.txt"
    subprocess.call(command, shell=True)

def do_priority_part(old_r1_service_b, old_r2_service_b, r1_b_new_limit, r2_b_new_limit):
    total_new_increase = r1_b_new_limit - old_r1_service_b + r2_b_new_limit - old_r2_service_b
    total_new_increase = int(total_new_increase * 0.8)
    high_priority_increase = int(total_new_increase * 0.7)
    low_priority_increase = total_new_increase - high_priority_increase
    if R1_PRIORITY > R2_PRIORITY:
        edit_key("r1_service_b", old_r1_service_b + high_priority_increase)
        edit_key("r2_service_b", old_r2_service_b + low_priority_increase)
    else:
        edit_key("r1_service_b", old_r1_service_b + low_priority_increase)
        edit_key("r2_service_b", old_r2_service_b + high_priority_increase)


# define query dict
CURRENT_REQUEST_SERVICE = "r1_service_b"
QUERY_SERVICE = CURRENT_REQUEST_SERVICE[-9:]

query_dict = {}
query_dict['service_a_rq_time'] = "service_a_cluster_service_a_upstream_rq_time"
query_dict['service_b_rq_time'] = "service_b_cluster_service_b_upstream_rq_time"
query_dict['service_c_rq_time'] = "service_c_cluster_service_c_upstream_rq_time"

# query_dict['rq_total'] = "service_a_cluster_service_a_upstream_rq_total"
# query_dict['rq_pending_total'] = "service_a_cluster_service_a_upstream_rq_pending_total"
# query_dict['rq_completed'] = "service_a_cluster_service_a_upstream_rq_completed"
# query_dict['rq_active'] = "service_a_cluster_service_a_upstream_rq_active"

query_dict['rq_total'] = QUERY_SERVICE + "_cluster_" + QUERY_SERVICE + "_upstream_rq_total"
query_dict['rq_pending_total'] = QUERY_SERVICE + "_cluster_" + QUERY_SERVICE + "_upstream_rq_pending_total"
query_dict['rq_completed'] = QUERY_SERVICE + "_cluster_" + QUERY_SERVICE + "_upstream_rq_completed"
query_dict['rq_active'] = QUERY_SERVICE + "_cluster_" + QUERY_SERVICE + "_upstream_rq_active"

def worker():
    Thread(target=init_vegeta).start()
    Thread(target=init_vegeta_v2).start()

    time.sleep(10)
    print("kill vegeta")
    kill_vegeta(CURRENT_TRAFFIC)
    kill_vegeta(CURRENT_TRAFFIC_V2)

    time.sleep(1)
    r1_throughput = get_throughput('./servicecb.txt')
    r2_throughput = get_throughput('./servicecb2.txt')
    current_overall_throughput = r1_throughput + r2_throughput


    # lstm part
    # current_stat_list = generate_metric(5, query_dict)
    # latency = get_mean_latency('./servicea.txt')
    # empty_stat_list = []
    # for i in range(len(current_stat_list)):
    #     current_stat_list[i]["mean_latency"] = latency
    #     empty_stat_list += [float(i) for i in list(current_stat_list[i].values())]
    
    # r1_b_new_limit = lstm_model("models/dl/r1_service_b_lstm", empty_stat_list)
    # exit()

    # get current stat
    current_stat = generate_metric(1, query_dict)[0]

    current_stat["mean_latency"] = get_mean_latency('./servicecb.txt')

    current_stat_val = [float(i) for i in list(current_stat.values())]
    r1_b_new_limit = r1_b_predictor(current_stat_val)
    # r1_b_new_limit = fc_model("models/dl/r1_service_b_fc", current_stat_val)

    r1_b_new_limit = int(r1_b_new_limit)
    if r1_b_new_limit < 0:
        return

    current_stat["mean_latency"] = get_mean_latency('./servicecb2.txt')
    current_stat_val = [float(i) for i in list(current_stat.values())]
    r2_b_new_limit = r2_b_predictor(current_stat_val)
    # r2_b_new_limit = fc_model("models/dl/r2_service_b_fc", current_stat_val)
    # r2_b_new_limit = lstm_model("models/dl/r2_service_b_lstm", empty_stat_list)


    r2_b_new_limit = int(r2_b_new_limit)
    if r2_b_new_limit < 0:
        return
    current_limit_dict = get_all_keys()
    old_r1_service_b = current_limit_dict["r1_service_b"]
    old_r2_service_b = current_limit_dict["r2_service_b"]

    current_limit_dict["r1_service_b"] = r1_b_new_limit
    current_limit_dict["r2_service_b"] = r2_b_new_limit


    predicted_throughput = checkerInfer([float(i) for i in list(current_limit_dict.values())])

    print("predicted_throughput: " + str(predicted_throughput))
    print("current_throughput: " + str(current_overall_throughput))
    print("Trying to edit descriptor " + "r1_service_b" + " from " + str(old_r1_service_b)
    + " To " + str(r1_b_new_limit))
    print("Trying to edit descriptor " + "r2_service_b" + " from " + str(old_r2_service_b)
    + " To " + str(r2_b_new_limit))

    if predicted_throughput >= current_overall_throughput:
        print("edit success")
        edit_key("r1_service_b", r1_b_new_limit)
        edit_key("r2_service_b", r2_b_new_limit)
    else:
        print("edit fail, try to apply partial rate")
        do_priority_part(old_r1_service_b, old_r2_service_b, r1_b_new_limit, r2_b_new_limit)

while(True):
    worker()
    time.sleep(20)