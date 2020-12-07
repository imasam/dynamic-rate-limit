import subprocess
from threading import Thread
import time
import argparse
from parseYaml import get_key

CURRENT_TRAFFIC = "130"
CURRENT_TRAFFIC_V2 = "120"
DOCKER_YAML = "../envoy_monitoring/docker-compose.yml"

# get key's current limit
def get_current_limit(current_request_service):
    return get_key(current_request_service)

def init_docker():
    command = "docker-compose -f " + DOCKER_YAML + " up"
    subprocess.call(command, shell=True)

def init_vegeta():
    command = "echo GET \"http://localhost:10000/request1\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC + " -duration=0 | vegeta report > out.txt"
    subprocess.call(command, shell=True)

def init_vegeta_v2():
    command = "echo GET \"http://localhost:10000/request2\" |" \
        "vegeta attack -rate=" + CURRENT_TRAFFIC_V2 + " -duration=0 | vegeta report > out2.txt"
    subprocess.call(command, shell=True)

if __name__ == "__main__":

    print("init docker")
    Thread(target=init_docker).start()
    time.sleep(25)
    print("init vegeta")
    Thread(target=init_vegeta).start()

    Thread(target=init_vegeta_v2).start()



