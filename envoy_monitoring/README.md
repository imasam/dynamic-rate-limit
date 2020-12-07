## Micro services monitoring with envoy service mesh, prometheus
### Setup


### Run  
1. `docker-compose build`    
2. `docker-compose up`  
3. Hit `localhost::10000/request1` and `localhost::10000/request2`to generate some traffic between the services
4. Visit `localhost:9090` for prometheus
