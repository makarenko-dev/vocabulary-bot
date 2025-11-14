from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import settings

engine = create_async_engine(
    settings.ASYNC_DB_URL,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
