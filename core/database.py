from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from core.config import get_settings

DATABASE_URL = get_settings().DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
