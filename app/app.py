from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .configuration import (
    APILoggingMiddleware,
    ErrorHandlingMiddleware,
    configure_sentry,
)
from .api import user_router, item_router
from .util import logger

# Configure Sentry
configure_sentry()

app = FastAPI(title="FastAPI Template", version="0.1.0", debug=True)

### ----------------- Middleware Configuration ----------------- ###
# Order in middleware matters
# The last middleware added is the first one to process the request and the last one to process the response.

logger.info("Setting up middleware")

# Last to process request, first to process response
app.add_middleware(ErrorHandlingMiddleware)

app.add_middleware(APILoggingMiddleware)


# CORS Configuration - First to process request, last to process response
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Set a custom list of origins, methods & headers
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


### ----------------- Routes Configuration ----------------- ###


@app.get("/live")
def server_live():
    return {"message": "server live"}


app.include_router(user_router)
app.include_router(item_router)


__all__ = ["app"]
