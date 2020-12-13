import trio
from collections import deque
from typing import Any
from . import ScheduledTask
from LoggingConfigurator import logger


class TaskObject(ScheduledTask):
    def __init__(self):
        super().__init__()
        self.name = "Delay Tester"
        self._msgs = deque(' nyarukoishi~')
        self.delay = 0.5

    async def _task(self) -> Any:
        logger.debug(f"<{self.name}> Delaying for {self.delay} second")
        await trio.sleep(self.delay)
        self._msgs.rotate(-1)
        return "".join(self._msgs)
