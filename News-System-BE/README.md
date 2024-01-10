1. Download gcloud CLI by following [here](https://cloud.google.com/sdk/docs/install)

2. Open Google Cloud SDK Shell, run
    ```
    gcloud init
    ```
    After finishing initialize gloud, then you can follow [here](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images) to push image to artifact registry, or try below. Remember to enable Artifact Registry API.

3. Create artifact reposotory
    ```
    gcloud artifacts repositories create [REPO_NAME] --repository-format=docker --location=us-central1 --description="Docker repository"
    ```
    and verify:
    ```
    gcloud artifacts repositories list
    ```

4. Configure authentication
    ```
    gcloud auth configure-docker us-central1-docker.pkg.dev
    ```

5. Tag the image 
    ```
    docker tag [DOCKER_IMAGE_NAME] us-central1-docker.pkg.dev/[PROJECT_NAME]/[REPO_NAME]/[IMAGE_NAME]:tag1
    ```

6. Push the image to Artifact Registry
    ```
    docker push us-central1-docker.pkg.dev/[PROJECT_NAME]/[REPO_NAME]/[IMAGE_NAME]:tag1
    ```

7. Create GKE cluster (remember to enable Kubernetes Engine API)
    ```
    gcloud container --project "news-database-55" clusters create-auto "autopilot-cluster-1" --region "us-central1" --release-channel "regular" --network "projects/news-database-55/global/networks/default" --subnetwork "projects/news-database-55/regions/us-central1/subnetworks/default" --cluster-ipv4-cidr "/17" --binauthz-evaluation-mode=DISABLED
    ```

8. Download `kubens` and `kubectx` [here](https://github.com/ahmetb/kubectx) for faster switch context and namespace. Then switch to right context and namespace
   ```
   kubectx [CONTEXT_NAME]
   kubens [NAMESPACE_NAME]
   ```
   then create Deployment
   ```
   kubectl apply -f deployment.yaml
   ```
   and Service
   ```
    kubectl apply -f service.yaml
   ```

9.  Now, you can access the website by getting IP address in EXTERNAL IP. Copy and run it in web browser.
    ```
    kubectl get service
    ```
    