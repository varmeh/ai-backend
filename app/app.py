from math import exp
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .configuration import logging_middleware
from .api import user_router, item_router
from .util import logger

app = FastAPI(title="FastAPI Template", version="0.1.0", debug=True)

### ----------------- Middleware Configuration ----------------- ###

logger.info("Setting up middleware")


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Set a custom list of origins, methods & headers
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.middleware("http")
async def logging(request: Request, call_next):
    return await logging_middleware(request, call_next)


### ----------------- Routes Configuration ----------------- ###


@app.get("/live")
def server_live():
    return {"message": "server live"}


app.include_router(user_router)
app.include_router(item_router)


__all__ = ["app"]
