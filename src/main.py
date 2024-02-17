from fastapi import FastAPI

app = FastAPI()


@app.get("/", include_in_schema=False)
def app_status() -> dict[str, str]:
    return dict(status="up")
