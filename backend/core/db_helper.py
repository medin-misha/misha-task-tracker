from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import settings


class DBHelper:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url)
        self.session_maker = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper: DBHelper = DBHelper(url=settings.db.url)
