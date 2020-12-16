import trio

# Kivy imports
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window

from InnerWidget import InnerWidget
import Loader

# Typing
from typing import List, Callable
from Schedules import ScheduledTask

# Temporary
from LoggingConfigurator import logger


class MainUI(BoxLayout):
    start_stop_wid = ObjectProperty()
    listing_layout: GridLayout = ObjectProperty()
    current_text = StringProperty()

    def __init__(self, send_channel, fn_accept_tasks, fn_stop_task, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.send_ch = send_channel
        self.widget_load_list = [str(n) for n in range(4)]
        self.loaded_widget_reference: List[InnerWidget] = []

        self.task_start: Callable = fn_accept_tasks
        self.task_stop: Callable = fn_stop_task

        self.multiplier = 0.3, 0.3
        self.listing_layout.size_hint_max = [mul_ * axis for mul_, axis in zip(self.multiplier, self.get_screen_size())]

    def on_start_release(self):
        logger.debug("Press Event on Start")
        if self.start_stop_wid.state == 'down':
            self.start_action()
        else:
            self.stop_action()

    def resize_grid(self, widget_count):
        # Temporary implementation, will fix

        rel_x, rel_y = self.multiplier
        x, y = self.get_screen_size()
        spacing = 10

        x_max = x // widget_count
        y_max = y // widget_count

        # pass this to InnerWidget

    def on_reload_release(self):
        """
        Clear and re-check python scripts in Schedules module and load them.
        :return:
        """
        self.stop_action()

        logger.debug("Press Event on Reload")
        self.listing_layout.clear_widgets()  # Drop widget first
        self.loaded_widget_reference.clear()  # Then drop reference!

        for task_object in Loader.fetch_scripts():
            self.loaded_widget_reference.append(InnerWidget(task_object, self.send_ch))
            self.listing_layout.add_widget(self.loaded_widget_reference[-1])
            logger.debug(f"Last added: {self.loaded_widget_reference[-1]}")

    def start_action(self):
        """
        Start scheduling execution of Task objects.
        """
        self.start_stop_wid.text = 'stop'
        self.task_start()
        for widget in self.loaded_widget_reference:
            logger.debug(f"Starting task {widget}")
            widget.submit_task()

    def stop_action(self):
        """
        Cancel the trio.CancelScope, stopping re-scheduling and execution of Task objects.
        """
        self.start_stop_wid.text = 'start'
        self.task_stop()

    @staticmethod
    def get_screen_size():
        return Window.size

class MainUIApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send_ch, self.recv_ch = trio.open_memory_channel(500)

        self.nursery: trio.Nursery = None
        self.cancel_scope: trio.CancelScope = None
        self.event: trio.Event = None

    def build(self):
        return MainUI(self.send_ch, self.start_tasks, self.cancel_tasks)

    def start_tasks(self):
        self.event.set()

    def cancel_tasks(self):
        logger.debug("Canceling Scope!")
        self.cancel_scope.cancel()

    async def app_func(self):
        """Trio wrapper async function."""

        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def run_wrapper():
                # Set trio
                await self.async_run(async_lib='trio')
                print("App Stop")
                nursery.cancel_scope.cancel()

            self.nursery.start_soon(self.wait_for_tasks, nursery)
            logger.debug("Starting UI")
            self.nursery.start_soon(run_wrapper)

    async def wait_for_tasks(self, nursery: trio.Nursery):
        async def scheduler():
            logger.debug("Now accepting tasks.")

            async with trio.open_nursery() as nursery_sub:
                async for task_coroutine in self.recv_ch:

                    nursery_sub.start_soon(task_coroutine)
                    logger.debug(f"Scheduled execution of task <{task_coroutine}>")

        while True:
            logger.debug(f"Now accepting tasks.")
            self.event = trio.Event()
            with trio.CancelScope() as cancel_scope:
                self.cancel_scope = cancel_scope
                await scheduler()
            try:
                while leftover := self.recv_ch.receive_nowait():
                    logger.debug(f"Dumping {leftover}")
            except trio.WouldBlock:
                pass

            logger.debug(f"Cancel scope closed, waiting for start event.")
            await self.event.wait()


if __name__ == '__main__':
    trio.run(MainUIApp().app_func)

