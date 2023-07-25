import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from ..util import logger


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as ex:
            # If any other type of exception is raised (an unexpected exception),
            # log it at the ERROR level and return a generic 500 error to the client.
            logger.error(
                f"Unhandled error occurred: {ex}",
                extra={
                    "errorDetails": {
                        "exceptionType": str(type(ex)),
                        "exceptionArguments": ex.args,
                        "stackTrace": traceback.format_exc(),
                    },
                },
            )
            return JSONResponse(
                status_code=500,
                content={"detail": str(ex)},
            )
        return response
