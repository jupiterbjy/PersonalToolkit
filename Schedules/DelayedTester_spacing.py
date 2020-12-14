import trio
from collections import deque
from typing import Any
from . import ScheduledTask


class TaskObject(ScheduledTask):
    def __init__(self):
        super().__init__()
        self.name = "Spacer"
        self._msgs = deque(' JUST FOR SPACING ')
        self.delay = 0.5

    async def _task(self) -> Any:
        await trio.sleep(self.delay)
        self._msgs.rotate(-1)
        return "".join(self._msgs)
