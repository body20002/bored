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
from api.activities.DTOs import ReadActivitiesDTO

from api.protocols import Filter, Paginator, Updater
from tables import activities as tables
from logger import logger


T_StrEnum = TypeVar("T_StrEnum", bound="StrEnum")


def get_default_values(enum: Type[T_StrEnum]) -> str:
    return f"Available values : {', '.join(enum._value2member_map_.keys())}"


@dataclass(slots=True, frozen=True)
class ActivityParameters:
    accessibility: tables.Accessibility | None = Parameter(
        tables.Accessibility | None,
        description=get_default_values(tables.Accessibility),
    )
    participants: tables.Participants | None = Parameter(
        tables.Participants | None,
        description=get_default_values(tables.Participants),
    )
    activity_type: tables.Type | None = Parameter(
        tables.Type | None,
        description=get_default_values(tables.Type),
        query="type",
    )
    duration: tables.Duration | None = Parameter(
        tables.Duration | None,
        description=get_default_values(tables.Duration),
    )
    price: tables.Price | None = Parameter(
        tables.Price | None,
        description=get_default_values(tables.Price),
    )
    kid_friendly: bool | None = Parameter(
        bool | None,
        description="Available Value : True, False",
    )

    def __call__(self):
        return asdict(self)


@dataclass(slots=True, frozen=True)
class ActivityUpdater(ActivityParameters):
    activity: str | None = Parameter(
        str | None,
    )
    link: str | None = Parameter(
        str | None,
    )

    def __call__(self, pk):
        # TODO: Return The Updated value
        return (
            update(tables.Activities)
            .where(tables.Activities.id == pk)
            .values({k: v for k, v in asdict(self).items() if v is not None})
        )


@dataclass(slots=True, frozen=True)
class ActivityFilter(ActivityParameters):
    def __call__(self, select):
        filters: list[ColumnElement[bool]] = []
        non_none_attributes = {k: v for k, v in asdict(self).items() if v is not None}
        filters.extend(getattr(tables.Activities, k) == v for k, v in non_none_attributes.items())
        return select.filter(*filters)


@dataclass(slots=True, frozen=True)
class ActivityPaginator:
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


class ActivitiesController(Controller):
    path = "/activities"
    dependencies = {
        "filters": Provide(ActivityFilter),
        "paginator": Provide(ActivityPaginator),
        "parameters": Provide(ActivityParameters),
        "updater": Provide(ActivityUpdater),
    }
    tags = ["Activities"]

    @get("/all", cache=True)
    async def all(
        self,
        async_session: AsyncSession,
        paginator: Paginator,
    ) -> Iterable[tables.Activities]:
        logger.info(f"Getting All Activities From {paginator.offset} To {paginator.limit + paginator.offset}")
        query = paginator(select(tables.Activities))
        return (await async_session.scalars(query)).all()

    @get("/{pk:int}")
    async def retrieve(
        self,
        async_session: AsyncSession,
        pk: int,
    ) -> tables.Activities:
        logger.info(f"Getting Activity with {pk = }")
        result = await async_session.get(tables.Activities, pk)

        if not result:
            raise HTTPException(detail="Activity with {pk = } doesn't exists", status_code=HTTP_404_NOT_FOUND)

        return result

    @get("/random")
    async def random(
        self,
        async_session: AsyncSession,
        filters: Filter,
    ) -> tables.Activities:
        logger.info(f"Getting A Random Activity With {filters = }")
        query = filters(select(tables.Activities))
        result = (await async_session.scalars(query)).all()
        return random.choice(result)

    @get("/", cache=True)
    async def filtered(
        self,
        async_session: AsyncSession,
        filters: Filter,
        paginator: Paginator,
    ) -> Iterable[tables.Activities]:
        logger.info(
            f"Getting All Activities With {filters = } From {paginator.offset} To {paginator.limit + paginator.offset}"
        )
        query = paginator(filters(select(tables.Activities)))
        return (await async_session.scalars(query)).all()

    @post("/create")
    async def create(
        self,
        async_session: AsyncSession,
        data: ReadActivitiesDTO,
    ) -> tables.Activities:
        activity: tables.Activities = data.to_model_instance()
        logger.info(f"Adding Activity with {data = }")
        async_session.add(activity)
        await async_session.commit()
        return activity

    @put("/{pk:int}")
    async def update(
        self,
        async_session: AsyncSession,
        pk: int,
        updater: Updater,
    ) -> None:
        # TODO: Return The Updated Activity: SQLite is limited and can't do it
        activity = await async_session.get(tables.Activities, pk)
        if activity is None:
            raise HTTPException(detail="No Entry Is Associated with this pk", status_code=HTTP_404_NOT_FOUND)

        _ = await async_session.execute(updater(pk=pk))
        async_session.expire(activity)

        await async_session.commit()

    @delete("/{pk:int}")
    async def delete(
        self,
        async_session: AsyncSession,
        pk: int,
    ) -> None:
        activity = await async_session.get(tables.Activities, pk)
        if activity is not None:
            await async_session.delete(activity)
            await async_session.commit()
