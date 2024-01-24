from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

from google_data_transfer.google_api.form import Form
from google_data_transfer.google_api.sheet import GoogleSpreadSheet, Worksheet


@dataclass
class TransferConfig(ABC):
    form_key: list[str]
    sheet_key: list[str]
    target_col: str
    name: str
    missing_fill_value: str

    @abstractmethod
    def transfer(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        ...

    @abstractmethod
    def match_rows(
        self, form: Form, sheet: GoogleSpreadSheet, worksheet: Worksheet
    ) -> dict:
        ...
