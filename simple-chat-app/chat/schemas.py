from pydantic import Field, BaseModel


class MessageRead(BaseModel):
    id: int = Field(..., description="Message ID")
    sender_id: int = Field(..., description="Sender ID")
    recipient_id: int = Field(..., description="Recipient ID")
    content: str = Field(..., description="Message content")


class MessageCreate(BaseModel):
    recipient_id: int = Field(..., description="Recipient ID")
    content: str = Field(..., description="Message content")
