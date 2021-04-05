import time
import trio
from . import ScheduledTask

"""
Minimal task for minimal testing purpose.
"""


class TaskObject(ScheduledTask):
    def __init__(self):
        super().__init__()
        self.name = "time.time()"

    async def task(self):
        await trio.sleep(0.1)
        return f"{time.time():.6f}"
