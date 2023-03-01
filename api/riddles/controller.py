import random
from collections.abc import Iterable
from dataclasses import dataclass, asdict
from typing import TypeVar, Type
from enum import StrEnum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm.interfaces import ColumnElement
from starlite import Controller, Provide, Parameter, HTTPException, get, post, put, delete
from starlite.status_codes import HTTP_404_NOT_FOUND
from api.riddles.DTOs import ReadRiddlesDTO

from api.protocols import Filter, Paginator, Updater
from tables import riddles as tables
from logger import logger


T_StrEnum = TypeVar("T_StrEnum", bound="StrEnum")


def get_default_values(enum: Type[T_StrEnum]) -> str:
    return f"Available values : {', '.join(enum._value2member_map_.keys())}"


@dataclass(slots=True, frozen=True)
class RiddleParameters:
    difficulty: tables.Difficulty | None = Parameter(
        tables.Difficulty | None, description=get_default_values(tables.Difficulty)
    )

    def __call__(self):
        return asdict(self)


@dataclass(slots=True, frozen=True)
class RiddleUpdater(RiddleParameters):
    question: str | None = Parameter(
        str | None,
    )
    answer: str | None = Parameter(
        str | None,
    )
    source: str | None = Parameter(
        str | None,
    )

    def __call__(self, pk):
        # TODO: Return The Updated value
        return (
            update(tables.Riddles)
            .where(tables.Riddles.id == pk)
            .values({k: v for k, v in asdict(self).items() if v is not None})
        )


@dataclass(slots=True, frozen=True)
class RiddleFilter(RiddleParameters):
    def __call__(self, select):
        filters: list[ColumnElement[bool]] = []
        non_none_attributes = {k: v for k, v in asdict(self).items() if v is not None}
        filters.extend(getattr(tables.Riddles, k) == v for k, v in non_none_attributes.items())
        return select.filter(*filters)


@dataclass(slots=True, frozen=True)
class RiddlePaginator:
    offset: int = Parameter(
        int,
        required=False,
        default=0,
        ge=0,
        multiple_of=5,
    )
    limit: int = Parameter(
        int,
        required=False,
        default=10,
        ge=0,
        multiple_of=5,
    )

    def __call__(self, select):
        return select.offset(self.offset).limit(self.limit)


class RiddlesController(Controller):
    path = "/riddles"
    dependencies = {
        "filters": Provide(RiddleFilter),
        "paginator": Provide(RiddlePaginator),
        "updater": Provide(RiddleUpdater),
    }
    tags = ["Riddles"]

    @get("/all", cache=True)
    async def all(
        self,
        async_session: AsyncSession,
        paginator: Paginator,
    ) -> Iterable[tables.Riddles]:
        logger.info(f"Getting All Riddles From {paginator.offset} To {paginator.limit + paginator.offset}")
        query = paginator(select(tables.Riddles))
        return (await async_session.scalars(query)).all()

    @get("/{pk:int}")
    async def retrieve(
        self,
        async_session: AsyncSession,
        pk: int,
    ) -> tables.Riddles:
        logger.info(f"Getting Riddle with {pk = }")
        result = await async_session.get(tables.Riddles, pk)

        if not result:
            raise HTTPException(detail="Riddle with {pk = } doesn't exists", status_code=HTTP_404_NOT_FOUND)

        return result

    @get("/random")
    async def random(
        self,
        async_session: AsyncSession,
        filters: Filter,
    ) -> tables.Riddles:
        logger.info(f"Getting A Random Riddle With {filters = }")
        query = filters(select(tables.Riddles))
        result = (await async_session.scalars(query)).all()
        return random.choice(result)

    @get("/", cache=True)
    async def filtered(
        self,
        async_session: AsyncSession,
        filters: Filter,
        paginator: Paginator,
    ) -> Iterable[tables.Riddles]:
        logger.info(
            f"Getting All riddles With {filters = } From {paginator.offset} To {paginator.limit + paginator.offset}"
        )
        query = paginator(filters(select(tables.Riddles)))
        return (await async_session.scalars(query)).all()

    @post("/create")
    async def create(
        self,
        async_session: AsyncSession,
        data: ReadRiddlesDTO,
    ) -> tables.Riddles:
        riddle: tables.Riddles = data.to_model_instance()
        logger.info(f"Adding Riddle with {data = }")
        async_session.add(riddle)
        await async_session.commit()
        return riddle

    @put("/{pk:int}")
    async def update(
        self,
        async_session: AsyncSession,
        pk: int,
        updater: Updater,
    ) -> None:
        # TODO: Return The Updated Riddle: SQLite is limited and can't do it
        riddle = await async_session.get(tables.Riddles, pk)
        if riddle is None:
            raise HTTPException(detail="No Entry Is Associated with this pk", status_code=HTTP_404_NOT_FOUND)

        _ = await async_session.execute(updater(pk=pk))
        async_session.expire(riddle)

        await async_session.commit()

    @delete("/{pk:int}")
    async def delete(
        self,
        async_session: AsyncSession,
        pk: int,
    ) -> None:
        riddle = await async_session.get(tables.Riddles, pk)
        if riddle is not None:
            await async_session.delete(riddle)
            await async_session.commit()
