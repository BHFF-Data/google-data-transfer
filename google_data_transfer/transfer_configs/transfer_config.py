from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd


@dataclass
class TransferConfig(ABC):
    match_col_form_name_to_sheet_name_map: dict[str, str]
    target_col: str
    name: str
    missing_fill_value: str

    @abstractmethod
    def transfer(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        ...

    @abstractmethod
    def match_rows(self, *args, **kwargs) -> dict:
        ...
