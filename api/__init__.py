import typing
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from starlite.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from starlite.utils import create_exception_response
from starlite import Starlite, Request, Response

from api.activities.controller import ActivitiesController
from api.facts.controller import FactsController
from api.riddles.controller import RiddlesController
from api.websites.controller import WebsitesController

from tables import add_data, create_tables, drop_tables, create_session
from logger import logger
from settings import load_config

from api.plugins import sqlalchemy_config, sqlalchemy_plugin

settings = load_config()


async def on_startup() -> None:
    engine: AsyncEngine = typing.cast(AsyncEngine, sqlalchemy_config.engine)
    await create_tables(engine)
    LocalSession = create_session(engine)
    await add_data(settings.JSON_DATA_DIR, LocalSession)


async def on_shutdown() -> None:
    engine = typing.cast(AsyncEngine, sqlalchemy_config.engine)
    await drop_tables(engine)


def logging_exception_handler(_: Request, exc: Exception) -> Response:
    """
    Logs exception and returns appropriate response.

    Parameters
    ----------
    _ : Request
        The request that caused the exception.
    exc :
        The exception caught by the Starlite exception handling middleware and passed to the
        callback.

    Returns
    -------
    Response
    """
    logger.error("Application Exception", exc_info=exc)
    return create_exception_response(exc)


app = Starlite(
    route_handlers=[
        ActivitiesController,
        FactsController,
        RiddlesController,
        WebsitesController,
    ],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: logging_exception_handler},
    plugins=[sqlalchemy_plugin],
)
