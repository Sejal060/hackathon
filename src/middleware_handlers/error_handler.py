from fastapi.responses import JSONResponse
from fastapi import Request
from ..schemas.response import APIResponse

async def api_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            message=str(exc),
            data=None
        ).dict()
    )