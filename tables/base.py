from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy.orm.base import Mapped

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
