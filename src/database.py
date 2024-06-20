import asyncio
from tokenize import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from config import settings
from typing import Annotated




sync_engin =create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo = True,
    # pool_size = 5,
    # max_overflow=10
)

async_engin =create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo = True,
    # pool_size = 5,
    # max_overflow=10
)
# синхронные включение
async def get_123_async():
    async with async_engin.connect() as conn:
        res =await conn.execute(text("SELECT 1,2,3 union select 4,5,6;"))
        print(f"{res.first()=}")

def get_123_sync():
    with sync_engin.connect() as conn:
        res = conn.execute(text("SELECT 1,2,3 union select 4,5,6;"))
        print(f"{res.first()=}")
str_12 = Annotated[str, 12]

session_factory = sessionmaker(sync_engin)
Base = declarative_base(metadata=MetaData())
Base.metadata.create_all(sync_engin)
async def main():
    async with async_sessionmaker(async_engin, expire_on_commit=False, class_=AsyncSession, autoflush=True, autocommit=True)() as session:
        async with session.begin():
            # Perform operations with the database
            result = await session.execute(text("SELECT 1,2,3 union select 4,5,6;"))
            print(f"{result.first()=}")

if __name__ == "__main__":
    asyncio.run(main())