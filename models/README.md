We provide comprehensive automative tools in this project.

## Dataset Collection
### option 1:
simply run ```main.py``` <num_of_limit>.
### option2:
run ```run_vegeta.py``` first to run the whole microservices and 2 vegeta threads,
wait for the system to be stablized (around 30s) and then run
```getdataset.py``` to generate the dataset. It could be very  time consuming.

you can change the param in config.py to specifiy which request type and service's metrics you want to collect.


## Models
In models directory, there are some files for the training purpose. Use  ```linear_regression.py```, ```fc.py``` and ```lstm.py``` you can train your custom models. 

We also provide pre-trained models under dl directory. Currently we set linear regression in code due to its good performance, but in comment we  provides options to call FC and LSTM.

## Apply Dynamic Rate Limit
run ```run_vegeta.py``` first to run the whole microservices with 2 vegeta threads, and wait for the system to be stablized (around 30s).

Then run service workflows, like ```workflow-service-\<service name\>.py```, which will periodically change the limits of ```service-\<service name\>```. We seperate workflows for different services, so you can choose to enable selected services or all of them.

