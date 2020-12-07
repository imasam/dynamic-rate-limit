from helper import generate_metric, get_throughput, get_mean_latency
from parseYaml import get_all_keys, edit_key, get_key
from threading import Thread
from getdataset import kill_vegeta
import time
import subprocess
from model import checkerInfer, r1_c_predictor, fc_model

CURRENT_TRAFFIC = "101"
CURRENT_TRAFFIC_V2 = "111"
FC_MODEL_DIR = "models/dl/r1_service_c_fc"
LSTM_MODEL_DIR = "models/dl/r1_service_c_lstm"

def init_vegeta():
    command = "echo GET \"http://localhost:10000/request1\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC + " -duration=0 | vegeta report > servicec.txt"
    subprocess.call(command, shell=True)

def init_vegeta_v2():
    command = "echo GET \"http://localhost:10000/request2\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC_V2 + " -duration=0 | vegeta report > servicec2.txt"
    subprocess.call(command, shell=True)


# define query dict
CURRENT_REQUEST_SERVICE = "r1_service_c"
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
    r1_throughput = get_throughput('./servicec.txt')
    r2_throughput = get_throughput('./servicec2.txt')
    current_overall_throughput = r1_throughput + r2_throughput

    # lstm part
    # current_stat_list = generate_metric(5, query_dict)
    # latency = get_mean_latency('./servicea.txt')
    # empty_stat_list = []
    # for i in range(len(current_stat_list)):
    #     current_stat_list[i]["mean_latency"] = latency
    #     empty_stat_list += [float(i) for i in list(current_stat_list[i].values())]
    
    # new_limit = lstm_model(LSTM_MODEL_DIR, empty_stat_list)
    # exit()

    # get current stat
    current_stat = generate_metric(1, query_dict)[0]
    current_stat["mean_latency"] = get_mean_latency('./servicec.txt')

    current_stat_val = [float(i) for i in list(current_stat.values())]

    new_limit = r1_c_predictor(current_stat_val)
    # new_limit = fc_model(FC_MODEL_DIR, current_stat_val)

    new_limit = int(new_limit)
    if new_limit < 0:
        return
    print("new_limit: ", str(new_limit))

    current_limit_dict = get_all_keys()
    old_limit = current_limit_dict[CURRENT_REQUEST_SERVICE]
    current_limit_dict[CURRENT_REQUEST_SERVICE] = new_limit

    predicted_throughput = checkerInfer([float(i) for i in list(current_limit_dict.values())])

    print("Trying to edit descriptor " + CURRENT_REQUEST_SERVICE + " from " + str(old_limit)
    + " To " + str(new_limit))
    print("predicted_throughput: " + str(predicted_throughput))
    print("current_throughput: " + str(current_overall_throughput))
    if predicted_throughput >= current_overall_throughput:
        print("Edit Sucess")
        edit_key(CURRENT_REQUEST_SERVICE, new_limit)
    else:
        print("Edit Fail")

while(True):
    worker()
    time.sleep(20)
