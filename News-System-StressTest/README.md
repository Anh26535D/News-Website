# This is the way to deploy Locust

## Please create cluster and artifact registry before.

1. Build, tag and push the image to artifact registry
    ```
    cd News-System-StressTest
    docker build -t locust-image .
    docker tag locust-image asia-southeast1-docker.pkg.dev/crested-aquifer-485713-v5/docker-repo/locust-image:tag1
    docker push asia-southeast1-docker.pkg.dev/crested-aquifer-485713-v5/docker-repo/locust-image:tag1 
    ```

2.  Using `kubens` and `kubectx` to switch to right context and namespace
    ```
    kubectx [CONTEXT_NAME]
    kubectl create namespace locust
    kubens locust
    ```

3. Create ConfigMap, Deployment and Service
    ```
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

4.  Now, you can access the website by getting IP address in EXTERNAL IP. You may wait for minutes to activate service..
    ```
    kubectl get service
    ```
    