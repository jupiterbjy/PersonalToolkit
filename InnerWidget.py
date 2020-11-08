import trio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label


class InnerWidget(ButtonBehavior, BoxLayout):
    label_top = ObjectProperty()
    label_mid = ObjectProperty()
    label_bottom = ObjectProperty()

    def __init__(self, name, task_queue: trio.MemorySendChannel, **kwargs):
        self.task_send_ch = task_queue
        self.orientation = 'vertical'

        self.name = name
        self.countdown = 5

        super().__init__(**kwargs)

    async def update(self):
        self.label_mid.text = "timer start"

        for i in range(self.countdown):
            self.label_bottom.text = str(self.countdown - i)
            await trio.sleep(1)
        self.label_bottom.text = '0'

        self.label_mid.text = 'timer Stop'

    def on_press(self):
        self.task_send_ch.send_nowait(self.update)

    def update_bg(self, color):
        print("Update background called")
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


if __name__ == '__main__':
    class InnerWidgetApp(App):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.nursery = None
            self.send_channel, self.recv_channel = trio.open_memory_channel(512)

        def build(self):
            return InnerWidget('some nice name', self.send_channel)

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


    trio.run(InnerWidgetApp().app_func)
