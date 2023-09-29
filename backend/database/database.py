from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import DEBUG, SQL_URL

async_engine = create_async_engine(SQL_URL)

async_session = async_sessionmaker(async_engine, autoflush=False, expire_on_commit=False)
async def get_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()

class Base(DeclarativeBase):
    id = Column(Integer, index=True, primary_key=True, )
