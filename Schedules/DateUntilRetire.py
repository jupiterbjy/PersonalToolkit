import datetime
import trio


"""
Calculates how many days / much percent point is left until end of
mandatory military service.
"""


class Parameter:
    """
    Provide housing for parameters that app will read and prompt users to fill out.
    """
    retire: str = '2020-12-22'
    format: str = '%Y-%m-%d'


async def task(mem_send: trio.MemorySendChannel):
    """
    Task to be scheduled on every cycle. All should be async functions regardless of
    whether function performs IO operations or not. Use MemChannel to send back result.
    """

    today = datetime.datetime.now()
    target = datetime.datetime.strptime(Parameter.format, Parameter.retire)

    diff = (target - today).seconds

    await mem_send.send(diff)
