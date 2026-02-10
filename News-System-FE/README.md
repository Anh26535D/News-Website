# News-System-FE-Refactor

This template should help get you started developing with Vue 3 in Vite.

## Deployment Steps

1.  **Build, tag and push the image to artifact registry**

    ```bash
    # Ensure you are in the News-System-FE directory
    docker build -t fe-image .
    docker tag fe-image us-central1-docker.pkg.dev/news-system-cloud-project/docker-repo/fe-image:tag1
    docker push us-central1-docker.pkg.dev/news-system-cloud-project/docker-repo/fe-image:tag1 
    ```

2.  **Switch to the right context and namespace**

    ```bash
    # kubectx [CONTEXT_NAME]
    kubens news-system
    ```

3.  **Add SSL certificate**

    Generate a self-signed certificate for testing/development purposes.

    ```bash
    # Create certs folder if it doesn't exist
    mkdir -p certs

    # Generate self-signed certificate
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout certs/privkey.pem -out certs/fullchain.pem -subj "/C=VN/ST=Hanoi/L=Hanoi/O=IT/CN=localhost"

    # Create Secret in the namespace
    kubectl create secret generic fe-ssl-cert --from-file=fullchain.pem=certs/fullchain.pem --from-file=privkey.pem=certs/privkey.pem -n news-system
    ```

4.  **Create ConfigMap, Deployment and Service**

    Make sure you have your `.env` file ready locally before running these commands.

    ```bash
    # Create env config map
    kubectl create configmap fe-config --from-env-file=.env -n news-system

    # Apply Nginx configuration
    kubectl apply -f fe-nginx-config.yaml

    # Apply Deployment and Service
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

5.  **Access the application**

    Get the external IP address of your service.

    ```bash
    kubectl get service
    ```

    Wait for the External IP to be assigned. Once assigned, you can access the website using `https://<EXTERNAL-IP>:8080`. Note that since we configured SSL, you should use HTTPS (though with a self-signed cert, the browser will warn you).