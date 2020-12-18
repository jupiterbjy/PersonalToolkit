from os.path import abspath, dirname
from os import listdir
from typing import List
import importlib

from LoggingConfigurator import logger
from Schedules import ScheduledTask

TASK_LOCATION = "Schedules"
LOCATION = abspath(dirname(abspath(__file__)) + "/" + TASK_LOCATION)
OBJECT_NAME = "TaskObject"


def _load_task_objects(file_name, object_name):
    module = importlib.import_module(f"{TASK_LOCATION}.{file_name}")
    importlib.reload(module)

    return getattr(module, object_name)()


def fetch_scripts() -> List[ScheduledTask]:
    logger.debug(f"Loader looking for scripts inside {LOCATION}")

    sources = [f.removesuffix(".py") for f in listdir(LOCATION) if f.endswith(".py")]
    sources.remove("__init__")

    logger.debug(f"Fetched {len(sources)}.")

    importlib.invalidate_caches()
    task_objects = [_load_task_objects(fn, OBJECT_NAME) for fn in sources]
    return task_objects


def mock_widget_numbers_patch(target_task, num) -> List[ScheduledTask]:
    """
    Replace fetch_scripts() to return single Task Object for given num.
    Originally had it's own code, but removed for simplicity and lack of need on optimization.
    Therefore, will not reload Task Objects.

    :param target_task: Task Object following ScheduleTask protocol
    :param num: Number of Task Object to return
    :return: List[ScheduledTask]
    """

    logger.debug(f"[Mock Patched] Fetched {num}.")
    return [target_task() for _ in range(num)]


def mock_patch(num):
    from sys import modules
    from functools import partial

    target = fetch_scripts()[0].__class__
    func = partial(mock_widget_numbers_patch, target, num)

    self_ = modules.get(__name__)
    logger.debug(f"Mock patched {fetch_scripts.__name__}.")
    setattr(self_, fetch_scripts.__name__, func)


mock_patch(30)
