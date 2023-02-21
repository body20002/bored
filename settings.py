from configparser import ConfigParser, SectionProxy
from getpass import getuser
from pathlib import Path
from sys import platform
import json
import os

from logger import logger

config = ConfigParser()
config["DEFAULT"] = {
    "DB_URL": "sqlite:///./db.sqlite",
    "JSON_DATA_DIR": str((Path(__file__) / "../JSON_DATA/").resolve()),
}


PROJECT_NAME = os.environ.get("PROJECT_NAME", Path(__file__).parent.stem)

OS_SPECIFIC_PATH = None
if platform in ["win32", "win64"]:
    OS_SPECIFIC_PATH = os.getenv("APPDATA")
elif platform == "linux":
    OS_SPECIFIC_PATH = os.getenv("XDG_CONFIG_HOME")
elif platform == "darwin":
    OS_SPECIFIC_PATH = ""
else:
    logger.error(f"Not A Supported Platform: {platform}")
    raise RuntimeError("Not A Supported System")

USE_LOCAL_CONFIG_DIR = True

USER_CONFIG_DIR = Path(os.environ.get("CONFIG_DIR", f"{OS_SPECIFIC_PATH}/{PROJECT_NAME}"))
LOCAL_CONFIG_DIR = Path(__file__).parent
CONFIG_DIR = LOCAL_CONFIG_DIR if USE_LOCAL_CONFIG_DIR else USER_CONFIG_DIR


def save_config(config: ConfigParser, /, config_filepath: Path):
    try:
        config_filepath.parent.mkdir(exist_ok=True)
        with config_filepath.open("w") as f:
            config.write(f)

    except Exception as e:
        logger.error(f"Couldn't Save The Config: {e}", exc_info=True)
        raise OSError(f"Couldn't Save The Config: {e}") from e


def create_config(config_filepath: Path, profile: str):
    config[profile] = config["DEFAULT"]
    return save_config(config, config_filepath=config_filepath)


def _load_config(config_filepath: Path, profile: str) -> SectionProxy:
    if not config_filepath.name.endswith(".ini"):
        logger.info("\033[48;5;9mWrong File Type\033[49m ... Creating A New Config File With `.ini` Suffix")
        return _load_config(config_filepath.with_suffix(".ini"), profile)

    logger.info("\033[48;5;12mLoading Config\033[49m")
    config.read(config_filepath)

    return config[profile]


def load_config(
    config_file: str = "config.ini",
    /,
    profile: str = getuser(),
    cache: dict[float, SectionProxy] = {},  # This is intentional for creating a cache
) -> SectionProxy:  # sourcery skip: default-mutable-arg
    config_filepath = CONFIG_DIR / config_file

    if not config_filepath.exists():
        logger.info("\033[48;5;12mFirst Time Launching The App\033[49m")
        create_config(config_filepath=config_filepath, profile=profile)

    last_time_modified_time = config_filepath.stat().st_mtime
    if result := cache.get(last_time_modified_time):
        logger.info("\033[48;5;22mCache Hit\033[49m")
        return result

    logger.info("\033[48;5;9mCache Miss\033[49m")
    cache.clear()  # clear cache
    cache[last_time_modified_time] = _load_config(config_filepath, profile)
    return cache[last_time_modified_time]


def reset_config(profile: str = getuser()) -> ConfigParser:
    config[profile] = config.defaults()
    return config


def serialize_config(config: ConfigParser, /, profile: str = getuser()):
    return json.dumps(dict(config[profile].items()))


def deserialize_config(serialized_config: str, /, profile: str = getuser()):
    data: dict[str, str] = json.loads(serialized_config)
    config = ConfigParser()
    config[profile] = data

    return config
