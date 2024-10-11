from typing import Any

from sqlalchemy import or_, and_, select

from database import BaseDAO, async_session_maker

from .models import Message


class MessageDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_messages_between_users(cls, user_id1: int, user_id2: int) -> Any:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter(
                    or_(
                        and_(
                            cls.model.sender_id == user_id1,
                            cls.model.recipient_id == user_id2,
                        ),
                        and_(
                            cls.model.sender_id == user_id2,
                            cls.model.recipient_id == user_id1,
                        ),
                    )
                )
                .order_by(cls.model.id)
            )
            result = await session.execute(query)
            return result.scalars().all()
