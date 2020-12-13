import time
from typing import Any
from . import ScheduledTask
from LoggingConfigurator import logger


"""
Minimal task for testing purpose.
"""


class TaskObject(ScheduledTask):
    def __init__(self):
        super().__init__()
        self.name = "time.time()"

    async def _task(self) -> Any:
        logger.debug("Running run_task")
        return f"{time.time():.6f}"
