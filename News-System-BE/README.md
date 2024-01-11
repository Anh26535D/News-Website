# This is the way to deploy Flask backend to the GKE. 

## Please create cluster and artifact registry before.

1. Build, tag and push the image to artifact registry
    ```
    cd News-System-BE
    docker build -t be-image .
    docker tag be-image us-central1-docker.pkg.dev/news-database-55/docker-repo/be-image:tag1
    docker push us-central1-docker.pkg.dev/news-database-55/docker-repo/be-image:tag1 
    ```

2.  Using `kubens` and `kubectx` to switch to right context and namespace
    ```
    kubectx [CONTEXT_NAME]
    kubectl create namespace flask-be
    kubens flask-be
    ```

3. Create ConfigMap, Deployment and Service
    ```
    kubectl create configmap be-config --from-env-file=.env
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

4.  Now, you can access the website by getting IP address in EXTERNAL IP. You may wait for minutes to activate service. **Use this with port 3030 to config in frontend**.
    ```
    kubectl get service
    ```
    