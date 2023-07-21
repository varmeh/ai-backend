from fastapi import FastAPI, APIRouter
from .util import to_camel_case
from .api import user_router, item_router

app = FastAPI()


@app.get("/live")
def server_live():
    return {"message": "server live"}


app.include_router(user_router)
app.include_router(item_router)


__all__ = ["app"]
