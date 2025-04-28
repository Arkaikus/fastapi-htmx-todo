 # Todo App with FastAPI HTMX and MongoDB

## Run locally

```bash
docker compose up -d --build
```

## Development
* Create a virtual environment
* Install dependencies with `pip install -r requirements.txt`
* Setup a `.env` file with the following:
```
MONGO_CONNECTION_STRING=mongodb://admin:password@localhost:27018/
```
* Run the mongo container with `docker compose up -d mongo`
* Run the app with `python .` or `uvicorn main:app --reload --host 0.0.0.0 --port 8000 --env-file .env`
