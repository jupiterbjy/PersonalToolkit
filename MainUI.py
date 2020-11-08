import trio
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty

from InnerWidget import InnerWidget


class MainUI(BoxLayout):
    start_stop_wid = ObjectProperty()
    listing_layout: GridLayout = ObjectProperty()
    current_text = StringProperty()

    def __init__(self, send_channel, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.send_ch = send_channel
        self.widget_load_list = [str(n) for n in range(4)]
        self.loaded_widget_reference = []

    def on_start_release(self):
        if self.start_stop_wid.state == 'down':
            self.start_stop_wid.text = 'stop'
            self.start_action()
        else:
            self.start_stop_wid.text = 'start'
            self.stop_action()

    def on_reload_release(self):
        print('a')
        self.listing_layout.clear_widgets()
        self.loaded_widget_reference.clear()  # Drop reference later!

        for name in self.widget_load_list:
            self.loaded_widget_reference.append(InnerWidget(name, self.send_ch))
            self.listing_layout.add_widget(self.loaded_widget_reference[-1])

    def start_action(self):
        pass

    def stop_action(self):
        pass


class MainUIApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nursery: trio.Nursery = None
        self.send_ch, self.recv_ch = trio.open_memory_channel(500)

    def build(self):
        return MainUI(self.send_ch)

    async def app_func(self):
        """Trio wrapper async function."""

        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def run_wrapper():
                # Set trio
                await self.async_run(async_lib='trio')
                print("App Stop")
                nursery.cancel_scope.cancel()

            self.nursery.start_soon(run_wrapper)
            self.nursery.start_soon(self.wait_for_tasks)

    async def wait_for_tasks(self):
        self.nursery: trio.Nursery

        async for task in self.recv_ch:
            self.nursery.start_soon(task)
            print(f"Scheduled execution of task {task}")


if __name__ == '__main__':
    trio.run(MainUIApp().app_func)

