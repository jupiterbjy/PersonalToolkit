import datetime
from typing import Any

from . import ScheduledTask

"""
Calculates how many days / much percent point is left until end of
mandatory military service.
"""


# TODO: allow each scripts to have respective .kv files.

class TaskObject(ScheduledTask):

    def __init__(self):
        super().__init__()
        self.name = "Served Ratio"
        self.parameters = {
            "Enroll": "2019-07-15",
            "Retire": "2020-12-20",
            "Format": "%Y-%m-%d"
        }
        self._storage = dict()

    async def _task(self) -> Any:
        today = datetime.datetime.now()

        try:
            start, end = self._storage["start_date"], self._storage["end_date"]

        except KeyError:  # Not calculated
            end = datetime.datetime.strptime(
                self.parameters["Retire"],
                self.parameters["Format"]
            )
            start = datetime.datetime.strptime(
                self.parameters["Enroll"],
                self.parameters["Format"]
            )
            self._storage["total_dur"] = (end - start).total_seconds()

            self._storage["start_date"], self._storage["end_date"] = start, end
            
        time_passed = (today - start).total_seconds()
        return f"{(time_passed * 100) / self._storage['total_dur']:.7f}%"
