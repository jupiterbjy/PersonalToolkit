import trio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior


class Root(BoxLayout):
    ref_1 = ObjectProperty()
    ref_2 = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Test(ButtonBehavior, BoxLayout):
    label_top = ObjectProperty()

    def __init__(self, name, send_ch: trio.MemorySendChannel, **kwargs):
        self.name = name
        self.send_ch = send_ch

        super().__init__(**kwargs)


class TestApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nursery = None
        self.send_channel, self.recv_channel = trio.open_memory_channel(512)

    def build(self):
        return Root()
        # return Root(self.send_channel)  # <<---

    async def app_func(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def wrapper():
                await self.async_run('trio')
                nursery.cancel_scope.cancel()

            nursery.start_soon(wrapper)


if __name__ == '__main__':
    trio.run(TestApp().app_func)
