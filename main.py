from pathlib import Path

from tables import add_data, create_tables, drop_tables

create_tables()
DATA = (Path(__file__) / "../JSON_DATA/").resolve()
add_data(data_dir=DATA)
drop_tables()
