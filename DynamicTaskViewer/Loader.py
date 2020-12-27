from os.path import abspath, dirname
from os import listdir
from typing import List, Union, Iterable
from itertools import zip_longest, cycle
import importlib

from LoggingConfigurator import logger
from Schedules import ScheduledTask

TASK_LOCATION = "Schedules"
LOCATION = abspath(dirname(abspath(__file__)) + "/" + TASK_LOCATION)
OBJECT_NAME = "TaskObject"


def _load_task_objects(file_name, object_name) -> Union[ScheduledTask, None]:
    """
    With file_name and object_name, load object_name from file_name module and return instance of it.
    If error was raised while importing script, then will return None instead.

    :param file_name: Name of Task Scripts
    :param object_name: env_var for Object name in Task Scripts.
    :return: ScheduledTask or None if error raised.
    """
    try:
        module = importlib.import_module(f"{TASK_LOCATION}.{file_name}")
    except SyntaxError as err:
        logger.critical(err)
        return
    except Exception as err:
        logger.critical(err)
        return

    importlib.reload(module)

    return getattr(module, object_name)()


def fetch_scripts() -> List[ScheduledTask]:
    """
    Dynamically search and load all scripts in TASK_LOCATION.

    WARNING: THIS WILL NOT RELOAD __init__.py! This is limitation of importlib.

    :return: List[ScheduledTask]
    """
    logger.debug(f"Loader looking for scripts inside {LOCATION}")

    sources = [f.removesuffix(".py") for f in listdir(LOCATION) if f.endswith(".py")]
    sources.remove("__init__")

    logger.debug(f"Fetched {len(sources)}.")

    importlib.invalidate_caches()
    task_objects = (_load_task_objects(fn, OBJECT_NAME) for fn in sources)
    return [task_object for task_object in task_objects if task_object is not None]  # Filter None


def mock_widget_numbers_patch(target_tasks: Iterable, num) -> List[ScheduledTask]:
    """
    Replace fetch_scripts() to return repeated Task Object for given num.
    Originally had it's own code, but removed for simplicity and lack of need on optimization.
    Therefore, will not reload Task Objects.

    :param target_tasks: Iterable yielding Task Objects following ScheduleTask protocol
    :param num: Number of Task Object to return
    :return: List[ScheduledTask]
    """

    widget_list = [target_task() for target_task, _ in zip(cycle(target_tasks), range(num))]
    logger.debug(f"[Mock Patched] Fetching {len(widget_list)} widgets.")
    return widget_list


def mock_patch(num, target=None):
    """
    Fetch one scripts and repeats *num* times.

    :param num: number of widgets to create
    :param target: name of script to load. if not specified, will use first loaded script.
    """
    from sys import modules
    from functools import partial

    script_list = fetch_scripts()

    if not target or target not in (cls.__module__.split(".")[-1] for cls in script_list):
        # Checking Module name - aka file name without directory name.

        logger.warning(f"Target is None or not found in script_list. "
                       f"Make sure Target is set to script's file name. "
                       f"Will iterate {len(script_list)} found widgets instead.")

        repeat_target = script_list

    else:
        for script in script_list:
            if script.__module__.split(".")[-1] == target:
                repeat_target = [script]
                break
        else:
            logger.warn(f"Target {target} is not found while loading. Possibly a bug?")
            repeat_target = [script_list[0]]

    func = partial(mock_widget_numbers_patch, [target.__class__ for target in repeat_target], num)

    self_ = modules.get(__name__)
    logger.debug(f"Mock patched {fetch_scripts.__name__}.")
    setattr(self_, fetch_scripts.__name__, func)


mock_patch(30)
