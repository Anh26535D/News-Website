# This is the way to deploy Consumer to the GKE. 

## Please create all BE, Kafka, FE first.

1. Change directory
    ```
    cd News-System-Tracking
    ```

2. Build, tag and push the image to artifact registry
    ```
    docker build -t consumer .
    docker tag consumer asia-southeast1-docker.pkg.dev/news-system-cloud-project/docker-repo/consumer:tag1
    docker push asia-southeast1-docker.pkg.dev/news-system-cloud-project/docker-repo/consumer:tag1 
    ```

3. Create Deployment for consumer.
    ```
    kubectl create configmap consumer-config --from-env-file=.env
    kubectl apply -f consumer.yaml
    ```
    