from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": exc.detail}, status_code=exc.status_code)
