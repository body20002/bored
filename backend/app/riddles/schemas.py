from pydantic import BaseModel

from .enums import Difficulty


class RiddleBaseModel(BaseModel):
    question: str
    answer: str
    difficulty: Difficulty
    source: str

    class Config:
        orm_mode = True


class Riddle(RiddleBaseModel):
    id: int


class RiddleIn(RiddleBaseModel):
    pass
