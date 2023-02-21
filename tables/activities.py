from enum import StrEnum, auto
from sqlalchemy.orm import Mapped, mapped_column
from tables.base import Base


class Accessibility(StrEnum):
    MAJOR_CHALLENGES = auto()
    MINOR_CHALLENGES = auto()
    FEW_TO_NO_CHALLENGES = auto()


class Participants(StrEnum):
    ALONE = auto()
    PARTY = auto()
    WITH_A_FRINED = auto()
    WITH_THE_GANG = auto()


class Type(StrEnum):
    BUSYWORK = auto()
    CHARITY = auto()
    COOKING = auto()
    DIY = auto()
    EDUCATION = auto()
    MUSIC = auto()
    RECREATIONAL = auto()
    RELAXATION = auto()
    SOCIAL = auto()


class Duration(StrEnum):
    HOURS = auto()
    MINUTES = auto()
    DAYS = auto()
    WEEK = auto()
    WEEKS = auto()


class Price(StrEnum):
    EXPENSIVE = auto()
    INEXPENSIVE = auto()
    FREE = auto()


class Activities(Base):
    activity: Mapped[str]
    kid_friendly: Mapped[bool]
    link: Mapped[str] = mapped_column(nullable=True)
    accessibility: Mapped[Accessibility]
    duration: Mapped[Duration]
    participants: Mapped[Participants]
    price: Mapped[Price]
    type: Mapped[Type]
