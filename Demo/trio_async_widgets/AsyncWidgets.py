import trio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


"""
An example used to figure out how to implement async calls for each widgets.
Was also test ground for setting background, text and outline colors.
Reference: https://stackoverflow.com/questions/48715092
"""


class AsyncWidget(ButtonBehavior, BoxLayout):
    label_top: Label = ObjectProperty()
    label_mid = ObjectProperty()
    label_bottom = ObjectProperty()

    def __init__(self, color, task_queue: trio.MemorySendChannel, **kwargs):
        self.task_send_ch = task_queue
        self.orientation = 'vertical'

        self.color = list(map(lambda x: x * 0.5, color))
        self.name = str(color)

        self.countdown = 3
        self.coroutine_running = False

        super().__init__(**kwargs)

    def update_bg(self, color):
        print("Update background called")
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self):
        self.rect.pos = self.pos
        self.rect.size = self.size

    async def update(self):
        with self.canvas.before:
            self.update_bg(list(i*1.5 for i in self.color))

        self.label_mid.text = "timer start"

        text_color, outline_color = self.label_mid.color, self.label_mid.outline_color
        self.label_mid.color = self.color

        self.label_mid.outline_width = 2
        self.label_mid.outline_color = (1, 1, 1, 1)

        for i in range(self.countdown):
            self.label_bottom.text = str(self.countdown - i)
            await trio.sleep(1)

        with self.canvas.before:
            self.update_bg(self.color)

        self.label_bottom.text = '0'

        self.label_mid.text = 'timer Stop'
        self.label_mid.color, self.label_mid.outline_color = text_color, outline_color
        self.label_mid.outline_width = 0

        self.coroutine_running = False

    def on_press(self):
        if self.coroutine_running:
            return

        self.coroutine_running = True
        self.task_send_ch.send_nowait(self.update)


class AsyncWidgetApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nursery = None
        self.send_channel, self.recv_channel = trio.open_memory_channel(512)

    def build(self):
        layout_main = BoxLayout()
        for color in ((1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)):
            layout_main.add_widget(AsyncWidget(color, self.send_channel))
        return layout_main

    async def app_func(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def wrapper():
                await self.async_run('trio')
                nursery.cancel_scope.cancel()

            nursery.start_soon(wrapper)
            nursery.start_soon(self.wait_for_tasks)

    async def wait_for_tasks(self):
        async for task in self.recv_channel:
            print(f"Task recv: {task} Type {type(task)}")
            self.nursery.start_soon(task)


if __name__ == '__main__':
    trio.run(AsyncWidgetApp().app_func)
