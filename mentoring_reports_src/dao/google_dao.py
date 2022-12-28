from abc import ABC, abstractmethod

import pandas as pd


class GoogleDAO(ABC):
    @abstractmethod
    def load_form_data(self, form_id: str) -> pd.DataFrame:
        ...

    def load_sheet_data(self, sheet_id: str, sheet_name: str) -> pd.DataFrame:
        ...
