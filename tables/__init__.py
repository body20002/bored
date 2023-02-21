import json
from pathlib import Path
from functools import lru_cache

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from tables.base import Base
from utils import import_all


import_all(__file__, globals(), __package__)

@lru_cache(maxsize=1)
def get_engine(url: str = "sqlite:///./db.sqlite", echo=False, **kwargs):
    return create_engine(
        url,
        echo=echo,
        **kwargs,
    )


def create_tables(engine: Engine = get_engine()):
    Base.metadata.create_all(engine)

def drop_tables(engine: Engine = get_engine()):
    Base.metadata.drop_all(engine)


def add_data(data_dir: Path, engine: Engine = get_engine()):
    tables = Base.metadata.tables
    for file in data_dir.glob("*.json"):
        try:
            if file.stem in tables:
                table = tables[file.stem]

                print(f"Adding Data To: {table.name}")
                data: list[dict] = json.loads(file.read_bytes())
                query = table.insert().values(data)

                with Session(engine) as session:
                    session.execute(query)
                    session.commit()
            print(f"{file.name} \033[48;5;22mOk\033[49m")
        except Exception as e:
            raise RuntimeError(f"\033[48;5;9mCouldn't Load file: {file}\033[49m") from e
