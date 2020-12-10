import trio
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty

from InnerWidget import InnerWidget
import Loader

# Typing
from typing import List
from Schedules import ScheduledTask

# Temporary
from LoggingConfigurator import LOGGER


class MainUI(BoxLayout):
    start_stop_wid = ObjectProperty()
    listing_layout: GridLayout = ObjectProperty()
    current_text = StringProperty()

    def __init__(self, send_channel, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.send_ch = send_channel
        self.widget_load_list = [str(n) for n in range(4)]
        self.loaded_widget_reference: List[InnerWidget] = []

    def on_start_release(self):
        LOGGER.debug("Press Event on Start")
        if self.start_stop_wid.state == 'down':
            self.start_stop_wid.text = 'stop'
            self.start_action()
        else:
            self.start_stop_wid.text = 'start'
            self.stop_action()

    def on_reload_release(self):
        LOGGER.debug("Press Event on Reload")
        self.listing_layout.clear_widgets()  # Drop widget first
        self.loaded_widget_reference.clear()  # Then drop reference!

        for task_object in Loader.fetch_scripts():

            self.loaded_widget_reference.append(InnerWidget(task_object, self.send_ch))
            self.listing_layout.add_widget(self.loaded_widget_reference[-1])
            LOGGER.debug(f"Last added: {self.loaded_widget_reference[-1]}")

    def start_action(self):
        for widget in self.loaded_widget_reference:
            LOGGER.debug(f"Starting task {widget}")
            widget.update()

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

            LOGGER.debug("Starting task receiver")
            self.nursery.start_soon(self.wait_for_tasks)
            LOGGER.debug("Starting UI")
            self.nursery.start_soon(run_wrapper)

    async def wait_for_tasks(self):
        self.nursery: trio.Nursery

        async for task in self.recv_ch:
            self.nursery.start_soon(task)
            LOGGER.debug(f"Scheduled execution of task {task}")


if __name__ == '__main__':
    trio.run(MainUIApp().app_func)

