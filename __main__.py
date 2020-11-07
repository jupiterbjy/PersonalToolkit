import trio
import kivy
kivy.require('2.0.0')

from AsyncApp import MainUIApp


if __name__ == '__main__':
    trio.run(MainUIApp().app_func)
