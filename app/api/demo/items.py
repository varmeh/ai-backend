from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from ...common import BaseModel


router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@router.get("/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}  # q is optional query parameter


@router.put("/{item_id}")
async def update_item(item_id: str, item: Item):
    return {"item": Item, "item_id": item_id}


## Http Exception from Code

items = {"foo": "The Foo Wrestlers"}


@router.get("/str/{item_id}")
async def read_item(item_id: str):
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
