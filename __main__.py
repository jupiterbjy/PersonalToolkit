import kivy
from kivy.app import App
from kivy.uix.label import Label

kivy.require('1.11.1')


class Test(App):
    def build(self):
        return Label(text='Sup')


if __name__ == '__main__':
    Test().run()
