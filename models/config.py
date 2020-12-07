
CURRENT_REQUEST_SERVICE = "r2_service_d"
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
