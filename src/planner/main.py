import dataclasses

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .core.exceptions import BaseError
from .users.routers import router as users_router

app = FastAPI()
app.include_router(users_router)


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, error: BaseError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=dataclasses.asdict(error),
    )


@app.get("/", include_in_schema=False)
def app_status() -> dict[str, str]:
    return dict(status="up")
