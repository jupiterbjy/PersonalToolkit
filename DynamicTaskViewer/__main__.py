import pretty_errors
import LoggingConfigurator
import trio
from MainUI import MainUIApp


if __name__ == "__main__":
    trio.run(MainUIApp().app_func)
