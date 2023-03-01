import random
from collections.abc import Iterable
from dataclasses import dataclass, asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from starlite import Controller, Provide, Parameter, HTTPException, get, post, put, delete
from starlite.status_codes import HTTP_404_NOT_FOUND
from api.websites.DTOs import ReadWebsitesDTO

from api.protocols import Paginator, Updater
from tables import websites as tables
from logger import logger


@dataclass(slots=True, frozen=True)
class WebsiteUpdater:
    url: str | None = Parameter(
        str | None,
    )
    description: str | None = Parameter(
        str | None,
    )

    def __call__(self, pk):
        # TODO: Return The Updated value
        return (
            update(tables.Websites)
            .where(tables.Websites.id == pk)
            .values({k: v for k, v in asdict(self).items() if v is not None})
        )


@dataclass(slots=True, frozen=True)
class WebsitePaginator:
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


class WebsitesController(Controller):
    path = "/websites"
    dependencies = {
        "paginator": Provide(WebsitePaginator),
        "updater": Provide(WebsiteUpdater),
    }
    tags = ["Websites"]

    @get("/", cache=True)
    async def all(
        self,
        async_session: AsyncSession,
        paginator: Paginator,
    ) -> Iterable[tables.Websites]:
        logger.info(f"Getting All Websites From {paginator.offset} To {paginator.limit + paginator.offset}")
        query = paginator(select(tables.Websites))
        return (await async_session.scalars(query)).all()

    @get("/{pk:int}")
    async def retrieve(
        self,
        async_session: AsyncSession,
        pk: int,
    ) -> tables.Websites:
        logger.info(f"Getting Website with {pk = }")
        result = await async_session.get(tables.Websites, pk)

        if not result:
            raise HTTPException(detail="Website with {pk = } doesn't exists", status_code=HTTP_404_NOT_FOUND)

        return result

    @get("/random")
    async def random(
        self,
        async_session: AsyncSession,
    ) -> tables.Websites:
        logger.info("Getting A Random Website")
        query = select(tables.Websites)
        result = (await async_session.scalars(query)).all()
        return random.choice(result)

    @post("/create")
    async def create(
        self,
        async_session: AsyncSession,
        data: ReadWebsitesDTO,
    ) -> tables.Websites:
        activity: tables.Websites = data.to_model_instance()
        logger.info(f"Adding Website with {data = }")
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
        # TODO: Return The Updated Website: SQLite is limited and can't do it
        activity = await async_session.get(tables.Websites, pk)
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
        activity = await async_session.get(tables.Websites, pk)
        if activity is not None:
            await async_session.delete(activity)
            await async_session.commit()
