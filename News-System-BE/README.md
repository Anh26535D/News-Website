1. Download gcloud CLI by following [here](https://cloud.google.com/sdk/docs/install)

2. Open Google Cloud SDK Shell, run
    ```
    gcloud init
    ```
    After finishing initialize gloud, then you can follow [here](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images) to push image to artifact registry, or try below. Remember to enable Artifact Registry API.

3. Create artifact reposotory
    ```
    gcloud artifacts repositories create docker-repo --repository-format=docker --location=us-central1 --description="Docker repository"
    ```
    and verify:
    ```
    gcloud artifacts repositories list
    ```

4. Configure authentication
    ```
    gcloud auth configure-docker us-central1-docker.pkg.dev
    ```

5. Build, tag and push the image to artifact registry
    ```
    cd News-System-BE
    docker build -t be-image .
    docker tag be-image us-central1-docker.pkg.dev/news-database-55/docker-repo/be-image:tag1
    docker push us-central1-docker.pkg.dev/news-database-55/docker-repo/be-image:tag1 
    ```

6. **[OPTIONAL]** Create GKE cluster (remember to enable Kubernetes Engine API)
    ```
    gcloud container --project "news-database-55" clusters create-auto "autopilot-cluster-1" --region "us-central1" --release-channel "regular" --network "projects/news-database-55/global/networks/default" --subnetwork "projects/news-database-55/regions/us-central1/subnetworks/default" --cluster-ipv4-cidr "/17" --binauthz-evaluation-mode=DISABLED
    ```

7.  Download `kubens` and `kubectx` [here](https://github.com/ahmetb/kubectx) for faster switch context and namespace. Then switch to right context and namespace
    ```
    kubectx [CONTEXT_NAME]
    kubectl create namespace flask-backend
    kubens flask-backend
    ```

8. Create ConfigMap, Deployment and Service
    ```
    kubectl create configmap backend-config --from-env-file=.env
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

9.  Now, you can access the website by getting IP address in EXTERNAL IP. Use this with port 3030 to config in frontend.
    ```
    kubectl get service
    ```
    