from os.path import abspath, dirname
from os import listdir
from typing import List
import importlib
import logging


TASK_LOCATION = "Schedules"
LOCATION = dirname(abspath(__file__)) + "/" + TASK_LOCATION
OBJECT_NAME = "TaskObject"
LOGGER = logging.getLogger("UI_DEBUG")


# TODO: look for proper type hinting


def fetch_scripts() -> List:
    LOGGER.debug(f"Loader looking for scripts inside {LOCATION}")

    sources = [f.removesuffix(".py") for f in listdir(LOCATION) if f.endswith(".py")]
    sources.remove("__init__")

    LOGGER.debug(str(sources))

    # FIX_NOW = perform relative import inside Schedules.

    task_objects = [getattr(importlib.import_module(f"{TASK_LOCATION}.{fn}"), OBJECT_NAME)()
                    for fn in sources]
    return task_objects

    # TODO: support dynamic reload of script in folder.


