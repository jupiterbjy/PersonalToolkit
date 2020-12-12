from typing import Callable


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
        self.output = "Empty"
        self._parameters = dict()

    def update_parameter(self, **kwargs):
        """
        No need to implement fail-safe, only keys in self.parameters will be shown on UI for editing.
        Will clear storage on value changes.
        """
        self._parameters.update(kwargs)

    async def run_task(self):
        """
        Originally planned to use Memory channel, but just storing results on self is sound.
        Will not check return data.
        """
        raise NotImplementedError

