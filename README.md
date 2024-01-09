1. The `mongo_compose.yaml` is optional if you use other mongodb instead of container. If you want to use docker container, run
    ```
    docker compose -f mongo_compose.yaml up -d
    ```

2. Create `.env` file in `News-System-BE/` by follow `.env.example` file, fetch data to mongodb and run server
    ```
    cd News-System-BE
    python3 -m pip install -r requirements.txt
    python generate_data.py
    python3 -m flask run
    ``` 
3. Create `.env` file in `News-System-FE/` by follow `.env.example` file, then open other terminal to run frontend
    ```
    cd News-System-FE
    npm install
    npm start
    ```
4. Open web browser and access `localhost:[PORT]`, where PORT can set in `.env` file in `News-System-FE/`