import json
from pathlib import Path
from functools import lru_cache

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from tables.base import Base
from utils import import_all
from logger import logger
from settings import load_config

settings = load_config()

import_all(__file__, globals(), __package__)


@lru_cache(maxsize=1)
def get_engine(echo=False, **kwargs):
    logger.info("Creating Database Enigne")
    return create_engine(
        settings["DB_URL"],
        echo=echo,
        **kwargs,
    )


def create_tables(engine: Engine = get_engine()):
    logger.info("Creating Database Tables")
    Base.metadata.create_all(engine)


def drop_tables(engine: Engine = get_engine()):
    logger.info("Dropping Database Tables")
    Base.metadata.drop_all(engine)


def add_data(data_dir: Path, engine: Engine = get_engine()):
    tables = Base.metadata.tables
    for file in data_dir.glob("*.json"):
        try:
            if file.stem in tables:
                table = tables[file.stem]

                logger.info(f"\033[48;5;12mAdding Data To:\033[49m {table.name}")
                data: list[dict] = json.loads(file.read_bytes())
                query = table.insert().values(data)

                with Session(engine) as session:
                    session.execute(query)
                    session.commit()
                logger.info(f"\033[48;5;22mData Loaded\033[49m From: {file.name}")
        except Exception as e:
            logger.error(f"\033[48;5;9mCouldn't Load file:\033[49m {file}", exc_info=True)
            raise RuntimeError(f"\033[48;5;9mCouldn't Load file: {file}\033[49m") from e
