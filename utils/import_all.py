from typing import Any
from logger import logger


# https://stackoverflow.com/a/60861023
def import_all(file: str, globals: dict[str, Any], package: str):
    from importlib import import_module
    from pathlib import Path

    for f in Path(file).parent.glob("*.py"):
        module_name = f.stem
        if (not module_name.startswith("_")) and (module_name not in globals):
            logger.info(f"Importing {package}.{module_name}")
            import_module(f".{module_name}", package)

        del f, module_name
    del import_module, Path
