import trio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

from Schedules import ScheduledTask


class InnerWidget(ButtonBehavior, BoxLayout):
    label_top = ObjectProperty()
    label_bottom = ObjectProperty()

    def __init__(self, task_object: ScheduledTask, mem_send: trio.MemorySendChannel, **kwargs):
        self.task_send_ch = mem_send
        self.orientation = 'vertical'

        self.task_object = task_object
        self.name = self.task_object.name

        self.rect = None

        super().__init__(**kwargs)

    def update(self):
        self.task_send_ch.send_nowait(self.task_object)

    def on_press(self):
        print(f"Press event on {self.name}")
        # self.task_send_ch.send_nowait(self.update)

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

