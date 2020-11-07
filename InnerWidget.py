import trio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior


class InnerWidget(ButtonBehavior, BoxLayout):

    def __init__(self, nursery: trio.Nursery, task_queue: trio.MemorySendChannel, **kwargs):
        super().__init__(**kwargs)
        self.nursery = nursery
        self.task_q = task_queue

        self.orientation = 'vertical'

        self.label_top = ObjectProperty()
        self.label_mid = ObjectProperty()
        self.label_bottom = ObjectProperty()

        self.countdown = 5

    async def update(self):
        self.label_mid.text("timer start")

        for i in range(self.countdown):
            await trio.sleep(1)
            self.label_bottom.text(self.countdown - i)

        self.label_mid.text('timer Stop')

    def on_press(self):
        print("Press event!")
        self.task_q.send_nowait(self.update)


if __name__ == '__main__':
    class InnerWidgetApp(App):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.nursery = None
            self.send_channel, self.recv_channel = trio.open_memory_channel(512)

        def build(self):
            return InnerWidget(self.nursery, self.send_channel)

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
                print(f"Task recv: {task}")
                await self.nursery.start_soon(task)


    trio.run(InnerWidgetApp().app_func)
