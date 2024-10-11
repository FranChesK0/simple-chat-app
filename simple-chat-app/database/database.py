from typing import Final
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DB_URL: Final[str] = "sqlite+aiosqlite:///db.sqlite3"
engine = create_async_engine(url=DB_URL)
async_session_maker: Final[async_sessionmaker] = async_sessionmaker(
    engine, class_=AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
