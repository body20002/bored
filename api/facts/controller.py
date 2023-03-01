import random
from collections.abc import Iterable
from dataclasses import dataclass, asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from starlite import Controller, Provide, Parameter, HTTPException, get, post, put, delete
from starlite.status_codes import HTTP_404_NOT_FOUND
from api.facts.DTOs import ReadFactsDTO

from api.protocols import Paginator, Updater
from tables import facts as tables
from logger import logger


@dataclass(slots=True, frozen=True)
class FactUpdater:
    fact: str | None = Parameter(
        str | None,
    )
    source: str | None = Parameter(
        str | None,
    )

    def __call__(self, pk):
        # TODO: Return The Updated value
        return (
            update(tables.Facts)
            .where(tables.Facts.id == pk)
            .values({k: v for k, v in asdict(self).items() if v is not None})
        )


@dataclass(slots=True, frozen=True)
class FactPaginator:
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


class FactsController(Controller):
    path = "/facts"
    dependencies = {
        "paginator": Provide(FactPaginator),
        "updater": Provide(FactUpdater),
    }
    tags = ["Facts"]

    @get("/", cache=True)
    async def all(
        self,
        async_session: AsyncSession,
        paginator: Paginator,
    ) -> Iterable[tables.Facts]:
        logger.info(f"Getting All Facts From {paginator.offset} To {paginator.limit + paginator.offset}")
        query = paginator(select(tables.Facts))
        return (await async_session.scalars(query)).all()

    @get("/{pk:int}")
    async def retrieve(
        self,
        async_session: AsyncSession,
        pk: int,
    ) -> tables.Facts:
        logger.info(f"Getting Fact with {pk = }")
        result = await async_session.get(tables.Facts, pk)

        if not result:
            raise HTTPException(detail="Fact with {pk = } doesn't exists", status_code=HTTP_404_NOT_FOUND)

        return result

    @get("/random")
    async def random(
        self,
        async_session: AsyncSession,
    ) -> tables.Facts:
        logger.info("Getting A Random Fact")
        query = select(tables.Facts)
        result = (await async_session.scalars(query)).all()
        return random.choice(result)

    @post("/create")
    async def create(
        self,
        async_session: AsyncSession,
        data: ReadFactsDTO,
    ) -> tables.Facts:
        activity: tables.Facts = data.to_model_instance()
        logger.info(f"Adding Fact with {data = }")
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
        # TODO: Return The Updated Fact: SQLite is limited and can't do it
        activity = await async_session.get(tables.Facts, pk)
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
        riddle = await async_session.get(tables.Facts, pk)
        if riddle is not None:
            await async_session.delete(riddle)
            await async_session.commit()
