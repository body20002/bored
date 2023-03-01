from starlite.plugins.sql_alchemy import SQLAlchemyConfig, SQLAlchemyPlugin
from starlite import DTOFactory

from settings import load_config

settings = load_config()

sqlalchemy_config = SQLAlchemyConfig(
    connection_string=settings.DB_URL,
    dependency_key="async_session",
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)


dto_factory = DTOFactory(plugins=[sqlalchemy_plugin])
