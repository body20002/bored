from pydantic.main import BaseModel

from .enums import (
    Accessibility,
    Duration,
    Price,
    Types,
    Participants,
)


class ActivityBase(BaseModel):
    activity: str
    kid_friendly: bool
    link: str
    accessibility: Accessibility
    duration: Duration
    participants: Participants
    price: Price
    type: Types

    class Config:
        orm_mode = True


class Activity(ActivityBase):
    id: int


class ActivityIn(ActivityBase):
    pass
