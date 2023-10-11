from orjson import loads, dumps, OPT_INDENT_2

from os import makedirs, urandom
from os.path import isdir, isfile

__EXAMPLE_CONFIG = {
    "host": "0.0.0.0",
    "port": 8080,
    "sql": "sqlite+aiosqlite:///./data.sqlite",
    "key": urandom(128).hex(),
    "data_dir": "data"
}

if not isfile("config.json"):
    with open("config.json", "wb") as config_file:
        config_file.write(dumps(__EXAMPLE_CONFIG, option=OPT_INDENT_2))

with open("config.json", "rb") as config_file:
    config: dict = loads(config_file.read())

HOST: str = config.get("host", "0.0.0.0")
PORT: int = config.get("port", 8080)
SQL_URL: str = config.get("sql", "sqlite+aiosqlite:///./data.sqlite")
KEY: str = config.get("key", __EXAMPLE_CONFIG["key"])
DATA_DIR: str = config.get("data_dir", "data")
DEBUG: bool = config.get("debug", False)

if not isdir(f"{DATA_DIR}/image"):
    makedirs(f"{DATA_DIR}/image")
# SQL_URL = "postgresql://user:password@postgresserver/db"
