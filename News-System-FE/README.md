## This is the way to deploy Nodejs frontend to the GKE. 

### Please deploy Backend and Kafka first.

1. Build, tag and push the image to artifact registry
    ```
    cd News-System-FE
    docker build -t fe-image .
    docker tag fe-image us-central1-docker.pkg.dev/news-database-55/docker-repo/fe-image:tag1
    docker push us-central1-docker.pkg.dev/news-database-55/docker-repo/fe-image:tag1 
    ```

2.  Using `kubens` and `kubectx` to switch to right context and namespace
    ```
    kubectx [CONTEXT_NAME]
    kubectl create namespace npm-fe
    kubens npm-fe
    ```

3. Create ConfigMap, Deployment and Service
    ```
    kubectl create configmap fe-config --from-env-file=.env
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

4.  Now, you can access the website by getting IP address in EXTERNAL IP. You may wait for minutes to activate service. **Use this with port 3300 to access the website**.
    ```
    kubectl get service
    ```
    