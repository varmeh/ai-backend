import time
import json
from os import environ as env
from typing import List, Union
from fastapi import Request, Response
from uuid import uuid4
from starlette.types import Message


from ..util import logger

_request_Id_key = "apiTrackingId"

LOG_API_DETAILED = env.get("LOG_API_DETAILED", "True").lower() == "true"


async def api_logging_middleware(request: Request, call_next):
    request_id = str(uuid4())
    logging_dict = {
        _request_Id_key: request_id  # X-API-REQUEST-ID maps each request-response to a unique ID
    }
    logging_dict["request"] = await _log_request(request, request_id)

    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()

    await _log_response(
        request=request,
        response=response,
        execution_time=end_time - start_time,
        logging_dict=logging_dict,
    )
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
    if not LOG_API_DETAILED:
        logger.info(
            f"@Api Request - {request.method} - {request.url.path}",
            extra={
                _request_Id_key: request_id,
                "request": request_data,
            },
        )
    else:
        # Log Request Detailed Information at debug level. This will be printed in development environments.
        # If you want to print this log in production environments as well, consider changing the logging level to logger.info
        request_data["headers"] = dict(request.headers)
        logger.info(
            f"@Api Request Detailed - {request.method} - {request.url.path}",
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


async def _log_response(
    request: Request, response: Response, execution_time: float, logging_dict: dict
):
    overall_status = "success" if response.status_code < 400 else "failure"

    response_logging = {
        "status": overall_status,
        "statusCode": response.status_code,
        "processingTime": f"{execution_time*1000:0.2}ms",
    }

    logging_dict["response"] = response_logging

    # Log Response Info at info level. This will be printed in all environments.
    if not LOG_API_DETAILED:
        logger.info(
            f"@Api Response - {request.method} - {request.url.path}",
            extra=logging_dict,
        )
    else:
        # Log Request Detailed Information at debug level. This will be printed in development environments.
        # If you want to print this log in production environments as well, consider changing the logging level to logger.info
        logging_dict["response"]["headers"] = dict(response.headers)
        logging_dict["response"]["body"] = await _extract_and_set_body(response)
        logger.info(
            f"@Api Response Detailed - {request.method} - {request.url.path}",
            extra=logging_dict,
        )


async def _extract_and_set_body(response: Response) -> Union[str, dict]:
    """Extracts the body from the response and resets the body_iterator
    for further usage by other parts of the code."""

    body_bytes = [section async for section in response.body_iterator]
    body_bytes_joined = b"".join(body_bytes)
    response.body_iterator = _AsyncIteratorWrapper(body_bytes)

    try:
        resp_body = json.loads(body_bytes_joined.decode())
    except json.JSONDecodeError:
        # If we can't decode the body as JSON, it might be a plain text
        resp_body = body_bytes_joined.decode(errors="replace")
    except UnicodeDecodeError:
        # If the body can't be decoded at all, use a placeholder
        resp_body = "<Could not decode body>"

    return resp_body


class _AsyncIteratorWrapper:
    """The following is a utility class that transforms a
    regular iterable to an asynchronous one.

    link: https://www.python.org/dev/peps/pep-0492/#example-2
    """

    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


__all__ = ["api_logging_middleware"]
