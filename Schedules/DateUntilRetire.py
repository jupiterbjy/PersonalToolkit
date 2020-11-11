import datetime
from . import ScheduledTask

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

    async def run_task(self):
        today = datetime.datetime.now()

        try:
            enroll, retire = self.storage["enroll_date"], self.storage["retire_date"]

        except KeyError:  # Not calculated
            retire = datetime.datetime.strptime(
                self.parameters["Format"],
                self.parameters["Retire"]
            )
            enroll = datetime.datetime.strptime(
                self.parameters["Format"],
                self.parameters["Retire"]
            )
            self.storage["service_duration"] = retire - enroll

            self.storage["enroll_date"], self.storage["retire_date"] = enroll, retire

        self.output = f"{(retire - today).seconds / self.storage['service_duration'].seconds:0.4f}"
