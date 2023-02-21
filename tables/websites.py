from sqlalchemy.orm import Mapped, mapped_column
from tables.base import Base


class Websites(Base):
    url: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]


