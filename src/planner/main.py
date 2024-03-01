from fastapi import FastAPI

from .users.routers import router as users_router

app = FastAPI()
app.include_router(users_router)


@app.get("/", include_in_schema=False)
def app_status() -> dict[str, str]:
    return dict(status="up")
