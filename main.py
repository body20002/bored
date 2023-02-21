from pathlib import Path

from tables import add_data, create_tables, drop_tables
from settings import load_config

settings = load_config()

create_tables()
DATA = Path(settings["JSON_DATA_DIR"]).resolve()
add_data(data_dir=DATA)
drop_tables()
