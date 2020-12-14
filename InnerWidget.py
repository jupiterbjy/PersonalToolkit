import trio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle, Canvas
from kivy.uix.label import Label

from Schedules import ScheduledTask
from LoggingConfigurator import logger

from typing import Iterable


class BackgroundManagerMixin:
    def update_bg(self, color: Iterable):
        self: BoxLayout

        self.canvas.before.clear()  # Is .before also canvas? I don't see method clear there.
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


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
        self.task_object._task_send_channel = mem_send

        self.name = self.task_object.name

        self.rect = None
        self.executed = 0
        self.bg_color = (0.5, 0.5, 0.5, 1)

        super().__init__(size_hint=(0.3, 0.3), **kwargs)

    def __str__(self):
        return f"<{self.__class__.__name__} Object based on {self.task_object.__module__}>"

    async def update_output(self):
        # Update called counter
        self.executed += 1
        self.executed_count = str(self.executed)

        # Catch any exceptions
        try:
            self.output = str(await self.task_object.run_task())
        except Exception as err:
            logger.critical(f"{self} encountered: {err}")
            self.output = "ERROR"
        finally:
            logger.debug(f"{self} done!")

            # And schedule self again
            await self.task_send_ch.send(self.update_output)

    def submit_task(self):
        self.task_send_ch.send_nowait(self.update_output)

    def on_press(self):
        print(f"Press event on {self.name}")
        # self.task_send_ch.send_nowait(self.submit_task)
