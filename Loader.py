from os.path import abspath, dirname
from os import listdir
import importlib


LOCATION = dirname(abspath(__file__)) + "/Schedules/"
OBJECT_NAME = "TaskObject"


def fetch_scripts():
    print("Loader looking for scripts inside", LOCATION)

    sources = [f for f in listdir(LOCATION) if f.endswith(".py")]
    sources.remove("__init__.py")

    task_objects = [getattr(importlib.import_module(fn), OBJECT_NAME)() for fn in sources]
    return task_objects

    # TODO: support dynamic reload of script in folder.


