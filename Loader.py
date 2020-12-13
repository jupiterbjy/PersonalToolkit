from os.path import abspath, dirname
from os import listdir
from typing import List
import importlib

from LoggingConfigurator import logger


TASK_LOCATION = "Schedules"
LOCATION = abspath(dirname(abspath(__file__)) + "/" + TASK_LOCATION)
OBJECT_NAME = "TaskObject"


def _load_task_objects(file_name, object_name):
    module = importlib.import_module(f"{TASK_LOCATION}.{file_name}")
    importlib.reload(module)

    return getattr(module, object_name)()


def fetch_scripts() -> List:
    logger.debug(f"Loader looking for scripts inside {LOCATION}")

    sources = [f.removesuffix(".py") for f in listdir(LOCATION) if f.endswith(".py")]
    sources.remove("__init__")

    logger.debug(f"Fetched {sources}")

    importlib.invalidate_caches()
    task_objects = [_load_task_objects(fn, OBJECT_NAME) for fn in sources]
    return task_objects
