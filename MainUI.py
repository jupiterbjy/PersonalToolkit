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
    listing_layout = ObjectProperty()
    current_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

    def on_start_release(self):
        if self.start_stop_wid.state == 'down':
            self.start_stop_wid.text = 'stop'
            self.start_action()
        else:
            self.start_stop_wid.text = 'start'
            self.stop_action()

    def on_reload_release(self):
        for _ in range(4):
            self.reload_action()

    def start_action(self):
        pass

    def stop_action(self):
        pass

    def reload_action(self):
        self.listing_layout: GridLayout
        self.listing_layout.clear_widgets()
        self.listing_layout.add_widget(InnerWidget())
        print("added widget")


class MainUIApp(App):

    nur = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loaded_list = []
        self.current_running = ''

    def build(self):
        return MainUI()

    async def app_func(self):
        """Trio wrapper async function."""

        async with trio.open_nursery() as nursery:
            self.nur = nursery

            async def run_wrapper():
                # Set trio
                await self.async_run(async_lib='trio')
                print("App Stop")
                nursery.cancel_scope.cancel()

            nursery.start_soon(run_wrapper)
            # nursery.start_soon(self.actions)

    async def actions(self):
        await trio.sleep(1000)


if __name__ == '__main__':
    trio.run(MainUIApp().app_func)

