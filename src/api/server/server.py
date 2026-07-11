from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.routes.accounts_routes import accounts_routes
from src.api.routes.users_routes import users_routes
from src.core.db import init_db

app = FastAPI(title="Sistema Bancário API")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> None:
    if exc.errors() and exc.errors()[0].get("type") == "json_invalid":
        return JSONResponse(
            status_code=422,
            content={"message": "JSON inválido", "detail": exc.errors()},
        )

    return JSONResponse(status_code=422, content={"detail": exc.errors()})


app.include_router(users_routes)
app.include_router(accounts_routes)

init_db()
