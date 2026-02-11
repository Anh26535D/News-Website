# This is the way to deploy Flask backend to the GKE. 

## Please create cluster and artifact registry before.

1. Build, tag and push the image to artifact registry
    ```
    cd News-System-BE
    docker build -t be-image .
    docker tag be-image asia-southeast1-docker.pkg.dev/news-system-cloud-project/docker-repo/be-image:tag1
    docker push asia-southeast1-docker.pkg.dev/news-system-cloud-project/docker-repo/be-image:tag1 
    ```

2. Create ConfigMap, Deployment and Service
    ```
    kubectl create configmap be-config --from-env-file=.env
    kubectl apply -f deployment.yaml
    kubectl apply -f hpa.yaml
    kubectl apply -f service.yaml
    ```

3.  Now, you can access the website by getting IP address in EXTERNAL IP. You may wait for minutes to activate service.
    ```
    kubectl get service
    kubectl get hpa -n news-system
    ```
    