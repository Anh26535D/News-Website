## This is the way to deploy Kafka to the GKE. 

### Please create cluster and artifact registry before

1. Change directory
    ```
    cd News-System-Kafka
    ```

2.  Using `kubens` and `kubectx` to switch to right context and namespace
    ```
    kubectx [CONTEXT_NAME]
    kubectl create namespace kafka
    kubens kafka
    ```

3. Create Deployment and Service for Zookeeper and Kafka.
    ```
    kubectl apply -f 01-zookeeper.yaml
    ```
    After create zookeeper service, you can find the clusterIP of zookeep by
    ```
    kubectl get svc
    ```
    , and put it in `02-kafka.yaml` file at env `KAFKA_ZOOKEEPER_CONNECT`. Then apply
    ```
    kubectl apply -f service.yaml
    ```
    