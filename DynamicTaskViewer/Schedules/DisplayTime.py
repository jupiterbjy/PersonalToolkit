import time
from typing import Any
from . import ScheduledTask

"""
Minimal task for testing purpose.
"""


class TaskObject(ScheduledTask):
    def __init__(self):
        super().__init__()
        self.name = "time.time()"

    async def _task(self) -> Any:
        return f"{time.time():.6f}"
