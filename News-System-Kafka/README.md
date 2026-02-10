# This is the way to deploy Kafka to the GKE. 

## Please create cluster and artifact registry before

1. Change directory
    ```
    cd News-System-Kafka
    ```

2.  Using `kubens` and `kubectx` to switch to right context and namespace
    ```
    kubectx [CONTEXT_NAME]
    kubens news-system
    ```

3. Create Deployment and Service for Zookeeper and Kafka.
    ```
    kubectl apply -f 01-zookeeper.yaml
    kubectl apply -f 02-kafka.yaml
    ```
    