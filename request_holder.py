import pandas as pd
from typing import Dict
from pandas import DataFrame


class RequestHolder:
    _requests_pull = pd.DataFrame()

    @property
    def requests_pull(self) -> DataFrame:
        return self._requests_pull

    def append(self, data: Dict):
        df = pd.DataFrame(data, index=["app_name"])
        self._requests_pull = self._requests_pull.append(df, ignore_index=True)
        print(f"Current pull: {self._requests_pull}")
        return "Request appended"

    def truncate(self):
        self._requests_pull = pd.DataFrame()
        return "Requests pull flushed"
