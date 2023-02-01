from abc import ABC, abstractmethod

import gspread
import pandas as pd
from google_data_transfer.commons import PathType


class Sheet(ABC):
    def __init__(self, spreadsheet_url: str, sheet_name: str):
        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet_id = spreadsheet_url.split("/")[-2]
        self.name = sheet_name

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def write_col(self, col_name: str, col_values: list) -> None:
        ...


class GSpreadSheet(Sheet):
    def __init__(self, spreadsheet_url: str, sheet_name: str, creds_path: PathType):
        super().__init__(spreadsheet_url, sheet_name)
        self.creds_path = creds_path
        # TODO: re-use auth token from auth.py
        self._gc = gspread.oauth(credentials_filename=creds_path)
        self._spreadsheet = self._gc.open_by_url(spreadsheet_url)
        self._sheet = self._spreadsheet.worksheet(sheet_name)
        self._df = self._to_df()

    def find_cells(self, query: str) -> list[gspread.Cell]:
        return self._sheet.findall(query)

    def _to_df(self) -> pd.DataFrame:
        return pd.DataFrame(self._sheet.get_all_records())

    def to_df(self) -> pd.DataFrame:
        return self._df

    def write_col(self, col_name: str, col_values: list) -> None:
        col_header_cells = self.find_cells(col_name)
        if len(col_header_cells) != 1:
            raise ValueError(
                f"Found {len(col_header_cells)} cells with name {col_name}."
            )
        col_header_cell = col_header_cells.pop()
        # Compute range in A1 notation
        col_a1 = col_header_cell.address.replace(str(col_header_cell.row), "")

        first_row_a1 = str(col_header_cell.row + 1)
        first_cell = col_a1 + first_row_a1

        num_rows = len(self._df)
        last_row_a1 = str(num_rows + 1)
        last_cell = col_a1 + last_row_a1

        update_range = first_cell + ":" + last_cell
        # Process col_values for gspread update
        update_values = [[el] for el in col_values]

        self._sheet.update(update_range, update_values)
