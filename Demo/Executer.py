import importlib
from os import listdir

CHECK_DIR = "target_sources"


class SourceCollection:
    def __init__(self):
        self.sources = {}
        self.update_sources()

    def update_sources(self):
        fetched = [i for i in listdir(CHECK_DIR) if "__main__.py" in listdir(f"{CHECK_DIR}/{i}")
         = [i for i in fetched if "__main__.py" in listdir(f"{CHECK_DIR}/{i}")]
        self.sourced
        for

        print(f"Loaded {len(self.sources)} Scripts.")

    def execute_script(self, target: str):
        if target not in self.sources:
            print(f"Script {target} does not exist.")
            return


