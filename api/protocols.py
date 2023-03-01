from typing import Any, Protocol, runtime_checkable
from sqlalchemy import Select, Update


@runtime_checkable
class Filter(Protocol):
    def __call__(self, select: Select) -> Select:
        ...


@runtime_checkable
class Updater(Protocol):
    def __call__(self, pk: int) -> Update:
        ...


@runtime_checkable
class Parameters(Protocol):
    def __call__(self) -> dict[str, Any]:
        ...


@runtime_checkable
class Paginator(Protocol):
    offset: int = 0
    limit: int = 10

    def __call__(self, select: Select) -> Select:
        ...
