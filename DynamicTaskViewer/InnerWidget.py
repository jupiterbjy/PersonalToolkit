import trio
import logging
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior

from KivyCustomModule import BackgroundManagerMixin
from Schedules import ScheduledTask


logger = logging.getLogger("debug")


class InnerWidget(ButtonBehavior, BoxLayout, BackgroundManagerMixin):
    """
    Display of task objects.
    """
    label_top = ObjectProperty()
    label_bottom = ObjectProperty()
    executed_count = StringProperty()
    output = StringProperty()

    def __init__(self, task_object: ScheduledTask, mem_send: trio.MemorySendChannel, **kwargs):
        self.task_send_ch = mem_send
        self.orientation = 'vertical'

        self.task_object = task_object

        self.name = self.task_object.name

        self.rect = None
        self.executed = 0
        self.bg_color = (0.5, 0.5, 0.5, 1)

        super().__init__(**kwargs)

    def __str__(self):
        return f"<{self.__class__.__name__} Object based on {self.task_object.__module__}>"

    async def update_output(self):
        # Update called counter
        self.executed += 1
        self.executed_count = str(self.executed)

        # Catch any exceptions
        try:
            result = await self.task_object.run_task()
        except Exception as err:
            logger.critical(f"{self} encountered: {err}")
            self.output = "ERR"
        else:
            if result is not None:
                self.output = str(result)

            # And schedule self again
            await self.task_send_ch.send(self.update_output)

    def submit_task(self):
        self.task_send_ch.send_nowait(self.update_output)

    def on_press(self):
        logger.debug(f"Press event on {self}")
        self.task_object.on_click()
