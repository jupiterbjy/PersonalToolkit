import datetime
from . import ScheduledTask
from LoggingConfigurator import logger

"""
Calculates how many days / much percent point is left until end of
mandatory military service.
"""


# TODO: allow each scripts to have respective .kv files.

class TaskObject(ScheduledTask):

    def __init__(self):
        super().__init__()
        self.name = "Service %"
        self.parameters = {
            "Enroll": "2019-07-15",
            "Retire": "2020-12-22",
            "Format": "%Y-%m-%d"
        }
        self._storage = dict()

    async def run_task(self):
        logger.debug("Task executed!")

        today = datetime.datetime.now()

        try:
            enroll, retire = self._storage["enroll_date"], self._storage["retire_date"]

        except KeyError:  # Not calculated
            retire = datetime.datetime.strptime(
                self.parameters["Retire"],
                self.parameters["Format"]
            )
            enroll = datetime.datetime.strptime(
                self.parameters["Enroll"],
                self.parameters["Format"]
            )
            self._storage["service_duration"] = retire - enroll
            logger.debug(self._storage["service_duration"])

            self._storage["enroll_date"], self._storage["retire_date"] = enroll, retire

        self.output = f"{(retire - today).total_seconds() / self._storage['service_duration'].total_seconds():0.4f}"

