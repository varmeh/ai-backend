from fastapi import Request
from uuid import uuid4
from starlette.types import Message


from ..util import logger

_request_Id_key = "X-API-REQUEST-ID"


async def logging_middleware(request: Request, call_next):
    request_id = str(uuid4())
    logging_dict = {
        _request_Id_key: request_id  # X-API-REQUEST-ID maps each request-response to a unique ID
    }
    logging_dict["request"] = await _log_request(request, request_id)
    response = await call_next(request)
    response.headers["X-Process-Time"] = "Testing"
    return response


# This function is responsible for logging the request details.
async def _log_request(request: Request, request_id: str) -> dict:
    path = request.url.path
    if request.query_params:
        path += f"?{request.query_params}"

    request_data = {
        "method": request.method,
        "path": path,
        "host": request.client.host,
    }

    request_data_orig = request_data.copy()

    # Get Request body for Post & Put requests
    if (
        request.method in ["POST", "PUT"]
        and request.headers.get("content-type") == "application/json"
    ):
        if "auth" in request.url.path:
            # If 'auth' is in the path, then set body as None.
            request_data["body"] = "Confidential"
        else:
            # use the modified set_body funct## Why do we need this method?
            # Body is receievd as a stream of data & once accessed in middleware, it could not be accessed in route & thus, this hack.ion to allow for request body to be logged
            await _receive_body_in_middleware(request)
            try:
                request_data["body"] = await request.json()
            except Exception as e:
                logger.debug(f"Couldn't extract body due to: {e}")

    # Log Request Info at info level. This will be printed in all environments.
    logger.info(
        f"@api request - {request.method} - {request.url.path}",
        extra={
            _request_Id_key: request_id,
            "request": request_data,
        },
    )

    # Log Request Detailed Information at debug level. This will be printed in development environments.
    # If you want to print this log in production environments as well, consider changing the logging level to logger.info
    request_data["headers"] = dict(request.headers)
    logger.debug(
        f"@api request - {request.method} - {request.url.path}",
        extra={
            _request_Id_key: request_id,
            "request": request_data,
        },
    )

    return request_data_orig


## Why do we need this method?
## Body is receievd as a stream of data & once accessed in middleware, it could not be accessed in route & thus, this hack.
async def _receive_body_in_middleware(self: Request):
    """
    Modifies FastAPI's default request._receive method to enable request body reading multiple times.

    It's not generally recommended to handle request body outside FastAPI routes. This method serves as a workaround
    to enable request body logging within middleware.

    This function changes a private attribute _receive of the Request object which is not a part of the public API,
    thus it might break with future versions of FastAPI or Starlette.

    This method reads the entire request body into memory which might be a problem for large request bodies.
    """

    # Save the original _receive method
    original_receive = self._receive

    # Define a custom receive method
    async def custom_receive() -> Message:
        nonlocal body
        if body is None:
            # body hasn't been read yet, read it from the original _receive
            message = await original_receive()
            body = message.get("body")
            return message
        else:
            # body has been read already, return it
            return {"type": "http.request", "body": body}

    body = None

    # Replace the original _receive method with the custom one
    self._receive = custom_receive


__all__ = ["logging_middleware"]
