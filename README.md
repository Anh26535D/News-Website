```
cd New-System-Apache-Hadoop
docker compose up -d

cd ..
cd News-System-BE
python3 -m pip install -r requirements.txt
python3 -m flask run

cd ..
cd News-System-FE
npm install
npm start
```