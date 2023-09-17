from uuid import uuid4
from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.core import Item
from models.database import get_db
from models.schemas import ItemCreate, ItemDelete


async def read_items(db: AsyncSession):
    return (await db.execute(select(Item))).scalars().all()


async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    uuid = str(uuid4())
    db_item = Item(uuid=uuid, text=item.text)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def read_limit_item(count: int, db: AsyncSession):
    return (await db.execute(select(Item).limit(count))).scalars().all()


async def read_item(uuid: str, db: AsyncSession = Depends(get_db)):
    result = await db.scalar(select(Item).where(Item.uuid == uuid))
    if not result:
        raise HTTPException(404, detail="Запись не найдена")
    return result


async def del_item(uuid: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(Item).where(Item.uuid == uuid))
    await db.commit()
    if result.rowcount < 1:
        raise HTTPException(404, detail="Запись не найдена")
    return ItemDelete(detail='Запись удалена')


