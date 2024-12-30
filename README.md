## Setup
Create a `env.json` file in root directory
```
{"DATABASE_URL":  }
```

## How to run
```
1. git clone https://github.com/sayansaha934/ecommerce-app.git
2. Create venv
3. pip install -r requirements.txt
4. python3 -m uvicorn main:app  --port 8005 --host 0.0.0.0 --reload
````

## Run using docker
```
docker-compose up -d
```
## Run tests

```
pytest tests/
```
