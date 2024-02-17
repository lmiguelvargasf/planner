from fastapi import FastAPI

from src.todo.schemas import HealthCheck

app = FastAPI()


@app.get("/", response_model=HealthCheck)
def app_status():
    return HealthCheck()
