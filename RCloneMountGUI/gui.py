"""
GUI definition of app
"""
import pathlib
from typing import TypedDict

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooser
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

import trio


kivy.require("2.0.0")


class Mount(TypedDict):
    # I didn't know this existed, what a nice feature!
    # https://www.python.org/dev/peps/pep-0589/
    letter: str
    share_name: str
    enabled: bool
    cache_dir: pathlib.Path
    cache_size: int
    type: str


class DirSelector(Popup):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, text_field: TextInput, **kwargs):
        super().__init__(**kwargs)
        self._text_field = text_field

    def select(self, path, selection):
        print(path, selection)
        self._text_field.text = selection[0]
        self.dismiss()


class EditPopUp(Popup):

    text_field: TextInput = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Nya"
        self.selector = DirSelector(self.text_field)


class EntryRow(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = EditPopUp()

    def show_popup(self):
        self._popup.open()


class GUI(BoxLayout):
    list_widget: GridLayout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.list_widget.bind(minimum_height=self.list_widget.setter('height'))
        self.widget_count = 0

    def add_row(self):
        new_obj = EntryRow()
        self.list_widget.add_widget(new_obj, self.widget_count)
        self.widget_count += 1


class GUIApp(App):

    def __init__(self, **kwargs):
        super(GUIApp, self).__init__(**kwargs)
        self._nursery = None
        self._send_channel, self._recv_channel = trio.open_memory_channel(512)

    def build(self):
        return GUI()


if __name__ == '__main__':
    app = GUIApp()
    app.run()
