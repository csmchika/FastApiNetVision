import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base


# for sync
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# for acync
Base = declarative_base()

engine = create_async_engine("sqlite+aiosqlite:///items.db", connect_args={"check_same_thread": False})
# engine = create_async_engine(os.getenv("FASTAPI_DB_URL"), connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
