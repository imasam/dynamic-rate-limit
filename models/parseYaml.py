import yaml
import os
import collections
import random
import time
from config import  CURRENT_REQUEST_SERVICE

YAML_FILE = '../envoy_monitoring/ratelimit_config.yaml'
start = 25
end = 200
def read_yaml(yaml_file):
    # read exist yaml
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as f:
            data = yaml.load(f)
        return data
    return None


# edit specific key's limit
def edit_key(key_val, to_edit):
    data = read_yaml(YAML_FILE)
    if data['descriptors'] == None:
        return
    
    for i in range(len(data['descriptors'])):
        if data['descriptors'][i]['value'] == key_val:
            data['descriptors'][i]['rate_limit']['requests_per_unit'] = to_edit
            with open(YAML_FILE,'w') as f:
                # print(data)
                f.write(yaml.dump(data))
            return

# get specific key's limit
def get_key(key_val):
    data = read_yaml(YAML_FILE)
    if data['descriptors'] == None:
        return
    
    for i in range(len(data['descriptors'])):
        if data['descriptors'][i]['value'] == key_val:
            return data['descriptors'][i]['rate_limit']['requests_per_unit']

# get all key's limit
def get_all_keys():
    data = read_yaml(YAML_FILE)
    if data['descriptors'] == None:
        return
    res = {}
    for i in range(len(data['descriptors'])):
        new_key = data['descriptors'][i]['value']
        key_val = data['descriptors'][i]['rate_limit']['requests_per_unit']
        res[new_key] = key_val
    # print(res)
    return res 

# random set all key except one key's limit
def random_set_all_except_one(key_val):
    data = read_yaml(YAML_FILE)
    if data['descriptors'] == None:
        return
    
    for i in range(len(data['descriptors'])):
        if data['descriptors'][i]['value'] == key_val:
            pass
        else:
            data['descriptors'][i]['rate_limit']['requests_per_unit'] = random.randint(start, end)

    with open(YAML_FILE,'w') as f:
        # print(data)
        f.write(yaml.dump(data))

    return 

# random set all key's limit
def random_set_all_key():
    data = read_yaml(YAML_FILE)
    if data['descriptors'] == None:
        return
    
    for i in range(len(data['descriptors'])):
            data['descriptors'][i]['rate_limit']['requests_per_unit'] = random.randint(start, end)

    with open(YAML_FILE,'w') as f:
        # print(data)
        f.write(yaml.dump(data))

    return

# start = time.time()
# edit_key('r1_service_b', 70)
# print(time.time()-start)
# print(get_key('r1_service_b'))
# random_set_all_except_one(CURRENT_REQUEST_SERVICE)
# get_all_keys()




