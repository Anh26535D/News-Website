### Requirements
1. Python
2. Node Package Manager: can be installed [here](https://nodejs.org/en/download)
3. Docker

### Usage
1. **[OPTIONAL]** You can ignore `mongo_compose.yaml` if you use other mongodb instead of container, otherwise, run
    ```
    docker compose -f mongo_compose.yaml up -d
    ```

2. Create `.env` file in `News-System-BE/` by following `.env.example` file, fetch data to mongodb and run server
    ```
    cd News-System-BE
    python3 -m pip install -r requirements.txt
    python generate_data.py # Optional
    python3 -m flask run
    ``` 
3. Create `.env` file in `News-System-FE/` by following `.env.example` file, then open other terminal to run frontend
    ```
    cd News-System-FE
    npm install
    npm start
    ```
4. Open web browser and access `localhost:[PORT]`, where PORT can set in `.env` file in `News-System-FE/`