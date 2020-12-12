import time
from . import ScheduledTask


"""
Minimal task for testing purpose.
"""


class TaskObject(ScheduledTask):

    async def run_task(self):
        pass
