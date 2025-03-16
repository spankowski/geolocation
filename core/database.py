from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel
from core.config import get_settings

# Ensure the database URL is properly formatted for asyncpg
DATABASE_URL = get_settings().DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency to get an async database session
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
