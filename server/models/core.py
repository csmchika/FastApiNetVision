from sqlalchemy.orm import Mapped, mapped_column
from models.database import Base


class Item(Base):
    __tablename__ = "items"

    uuid: Mapped[str] = mapped_column(primary_key=True, unique=True)
    text: Mapped[str] = mapped_column()
