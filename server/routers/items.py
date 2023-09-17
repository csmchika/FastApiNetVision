from typing import List

from fastapi import APIRouter

from controllers.items import *
from models.schemas import *

router = APIRouter()


@router.get("/all", response_model=List[ItemSchema])
async def get_items(db: AsyncSession = Depends(get_db)):
    return await read_items(db)


@router.post("/new", response_model=ItemSchema)
async def post_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item(item, db)


@router.get("/{count:int}", response_model=List[ItemSchema])
async def get_limit_items(count: int, db: AsyncSession = Depends(get_db)):
    return await read_limit_item(count, db)


@router.get("/{uuid:str}", response_model=ItemSchema)
async def get_item(uuid: str, db: AsyncSession = Depends(get_db)):
    return await read_item(uuid, db)


@router.delete("/{uuid}", response_model=ItemDelete)
async def delete_item(uuid: str, db: AsyncSession = Depends(get_db)):
    return await del_item(uuid, db)


