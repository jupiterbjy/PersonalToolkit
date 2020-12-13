import trio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

from Schedules import ScheduledTask
from LoggingConfigurator import logger


class InnerWidget(ButtonBehavior, BoxLayout):
    """
    Display of task objects.
    """
    label_top = ObjectProperty()
    label_bottom = ObjectProperty()
    output = StringProperty()

    def __init__(self, task_object: ScheduledTask, mem_send: trio.MemorySendChannel, **kwargs):
        self.task_send_ch = mem_send
        self.orientation = 'vertical'

        self.task_object = task_object
        self.task_object._task_send_channel = mem_send

        self.name = self.task_object.name

        self.rect = None

        super().__init__(**kwargs)

    def __str__(self):
        return f"<{self.__class__.__name__} Object based on {self.task_object.__module__}>"

    async def update_output(self):
        try:
            self.output = str(await self.task_object.run_task())
        except Exception as err:
            logger.critical(f"{self} encountered: {err}")
            self.output = "ERROR"
        finally:
            logger.debug(f"{self} done!")
            await self.task_send_ch.send(self.update_output)

    def submit_task(self):
        self.task_send_ch.send_nowait(self.update_output)

    def on_press(self):
        print(f"Press event on {self.name}")
        # self.task_send_ch.send_nowait(self.submit_task)

    def update_bg(self, color):
        print(f"Update background called on {self.name}")
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

