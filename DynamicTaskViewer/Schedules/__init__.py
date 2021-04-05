import logging
import trio

logger = logging.getLogger("debug")


class ScheduledTask:
    """
    Interface for task units.

    # Below description is plan, not implemented

    self.parameters dict only receives string inputs,
    it's up to user to convert param as they desire.
    """

    def __init__(self):
        """
        Script will check output periodically.
        """
        self.name = ""
        self._parameters = dict()
        self.run = True

    def update_parameter(self, **kwargs):
        """
        No need to implement fail-safe, only keys in self.parameters will be shown on UI for editing.
        Will clear storage on value changes.
        """
        self._parameters.update(kwargs)

    async def task(self):
        """
        Fill out your own actions here. Return value will be displayed on widget.
        """

        return None

    async def run_task(self):
        """
        Wrapper for task to add default click behavior.
        """

        # This way, there will be so many if branches per update!
        if self.run:
            return await self.task()

        await trio.sleep(2)

    def on_click(self):
        """
        Action to do when widget is pressed.
        """
        self.run = not self.run

