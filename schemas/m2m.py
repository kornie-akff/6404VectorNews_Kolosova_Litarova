from pydantic import BaseModel
from schemas.tag import TagOut

class TagSubscriptionOut(BaseModel):
    tag: TagOut
    is_notification_on: bool
    class Config:
        from_attributes = True

class NotificationSettingUpdate(BaseModel):
    enabled: bool

class LikeAction(BaseModel):
    user_id: int