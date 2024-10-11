from typing import Any, Dict

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from .database import Base, async_session_maker


class BaseDAO:
    model: Any = Base

    @classmethod
    async def find_all(cls, **filter_by: Dict[str, Any]) -> Any:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_id(cls, id: int) -> Any:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by(cls, **filter_by: Dict[str, Any]) -> Any:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values: Dict[str, Any]) -> Any:
        async with async_session_maker() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance
