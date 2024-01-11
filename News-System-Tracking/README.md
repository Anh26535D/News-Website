## This is the way to deploy Consumer to the GKE. 

### Please create all BE, Kafka, FE first.

1. Change directory
    ```
    cd News-System-Tracking
    ```

2. Build, tag and push the image to artifact registry
    ```
    docker build -t consumer .
    docker tag consumer us-central1-docker.pkg.dev/news-database-55/docker-repo/consumer:tag1
    docker push us-central1-docker.pkg.dev/news-database-55/docker-repo/consumer:tag1 
    ```

3.  Using `kubens` and `kubectx` to switch to right context and namespace
    ```
    kubectx [CONTEXT_NAME]
    kubectl create namespace consumer
    kubens consumer
    ```

4. Create Deployment for consumer.
    ```
    kubectl apply -f consumer.yaml
    ```
    