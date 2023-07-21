from ast import alias
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Body, Path

# from app.common import BaseModel
from pydantic import BaseModel


router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    name: str
    price: float
    isOffer: bool | None = Body(alias="isOffer")


@router.get("/{itemId}")
def read_item(item_id: Annotated[str, Path(alias="itemId")], q: str | None = None):
    return {"itemId": item_id, "q": q}  # q is optional query parameter


@router.put("/{itemId}")
async def update_item(item_id: Annotated[str, Path(alias="itemId")], item: Item):
    return {"itemId": item_id, "item_id": item.is_offer}


## Http Exception from Code

items = {"foo": "The Foo Wrestlers"}


@router.get("/str/{itemId}")
async def read_item(item_id: Annotated[str, Path(alias="itemId")]):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


## Dependency Injection


async def common_parameters(q: str | None = None, page: int = 0, limit: int = 100):
    return {"q": q, "page": page, "limit": limit}


@router.get("/commons/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


# export as item router
item_router = router

__all__ = ["item_router"]
