from sqlalchemy.orm import Mapped
from tables.base import Base


class Facts(Base):
    fact: Mapped[str]
    source: Mapped[str]

