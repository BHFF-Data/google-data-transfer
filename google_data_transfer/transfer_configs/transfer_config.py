import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd
from google_data_transfer.commons import PathType


def make_config_id(name: str) -> str:
    return name.lower().replace(" ", "_")


@dataclass
class TransferConfig:
    TransferFunctionType = Callable[[pd.DataFrame], pd.DataFrame]
    columns_join_map: dict[str:str]
    target_col: str
    name: str
    transfer_function: TransferFunctionType
    _id: str

    def __init__(
        self,
        columns_join_map: dict[str:str],
        target_col: str,
        name: str,
        transfer_function: TransferFunctionType,
    ):
        self.columns_join_map = columns_join_map
        self.target_col = target_col
        self.name = name
        self.transfer_function = transfer_function
        self._id = make_config_id(name)

    def to_pickle(self, config_dir_path: PathType) -> None:
        pickled_name = self._id + ".pickle"
        pickled_path = Path(config_dir_path) / pickled_name
        with open(pickled_path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def from_pickle(cls, pickled_path: PathType):
        with open(pickled_path, "rb") as file:
            config = pickle.load(file)
        return config
