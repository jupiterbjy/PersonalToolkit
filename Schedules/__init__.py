from typing import Callable, Any
from trio import MemorySendChannel


class ScheduledTask:
    """
    Abstract Protocol for task units.
    self.parameters dict only receives string inputs,
    it's up to user to convert param as they desire.
    """

    def __init__(self):
        """
        Script will check output periodically.
        """
        self.name = "NoName"
        self._task_send_channel: MemorySendChannel = None
        self._parameters = dict()

    def update_parameter(self, **kwargs):
        """
        No need to implement fail-safe, only keys in self.parameters will be shown on UI for editing.
        Will clear storage on value changes.
        """
        self._parameters.update(kwargs)

    async def run_task(self):
        """
        Tries to run task asynchronously, returns result or err if any happened.
        Schedule execution of self for continuous execution.
        :return:
        """
        try:
            return await self._task()
        except Exception as err:
            return err
        finally:
            await self._task_send_channel.send(self)

    async def _task(self) -> Any:
        """
        Fill out your own actions here. Not yet decided what to do with return value.
        """
        raise NotImplementedError

