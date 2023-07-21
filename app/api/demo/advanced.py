## File Upload
from typing import Annotated
from fastapi import APIRouter, UploadFile, Depends
from enum import Enum

router = APIRouter()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


async def common_parameters(q: str | None = None, page: int = 0, limit: int = 100):
    return {"q": q, "page": page, "limit": limit}


@router.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# export as user router
user_router = router
__all__ = ["user_router"]
