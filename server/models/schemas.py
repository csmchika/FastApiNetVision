from pydantic import BaseModel
from uuid import UUID


class ItemBase(BaseModel):
    text: str


class ItemCreate(ItemBase):
    pass


class ItemSchema(ItemBase):
    text: str
    uuid: UUID

    class Config:
        from_attributes = True


class ItemDelete(BaseModel):
    detail: str
