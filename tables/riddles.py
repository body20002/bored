from enum import StrEnum, auto
from sqlalchemy.orm import Mapped
from tables.base import Base

class Difficulty(StrEnum):
    EASY = auto()
    NORMAL = auto()
    HARD = auto()


class Riddles(Base):
    question: Mapped[str]
    answer: Mapped[str]
    difficulty: Mapped[Difficulty]
    source: Mapped[str]


