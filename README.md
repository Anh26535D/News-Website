# News website with Kafka for behaviour tracking

This project combines a Flask backend, Node.js frontend, Kafka messaging system, and MongoDB database to create a comprehensive news website. The use of Kafka allows for efficient behavior tracking, ensuring a seamless experience for both users and administrators.

This project contains 4 main modules:
 - Backend
 - Frontend
 - Kafka
 - Tracking

## Prerequisites
1. Python 3.9 or higher
2. Node Package Manager: can be installed [here](https://nodejs.org/en/download)
3. Docker
4. Google Cloud Account with activated billing (You can use visa card for trial)
5. MongoDB Atlas

## Installation

### First, you need to set up with GCP (Google Cloud Platform)
1. Download gcloud CLI by following [here](https://cloud.google.com/sdk/docs/install)

2. Open Google Cloud SDK Shell, run
    ```
    gcloud init
    ```
    You can find the tutorial by Google Cloud for completing the initialization.

3. Create artifact reposotory. This likes private docker registry (Docker Hub)
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

5. Create GKE cluster (remember to enable Kubernetes Engine API)
    ```
    gcloud container --project "[PROJECT_ID]" clusters create-auto "autopilot-cluster-1" --region "us-central1" --release-channel "regular" --network "projects/[PROJECT_ID]/global/networks/default" --subnetwork "projects/[PROJECT_ID]/regions/us-central1/subnetworks/default" --cluster-ipv4-cidr "/17" --binauthz-evaluation-mode=DISABLED
    ```

6.  Download `kubens` and `kubectx` [here](https://github.com/ahmetb/kubectx) for faster switch context and namespace.

### Next, you will set up `.env` file by following the `.env.example` in each module. Follow all step in each module to deploy to GKE. Following this
1. News-System-BE
2. News-System-Kafka
3. News-System-FE
4. News-System-Tracking