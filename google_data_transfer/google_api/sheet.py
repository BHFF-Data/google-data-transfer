from abc import ABC, abstractmethod

import gspread
import pandas as pd

from google_data_transfer.commons import PathType, compute_google_resource_id_from_url


class Sheet(ABC):
    spreadsheet_id: str
    name: str

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def write_col(self, col_name: str, col_values: list) -> None:
        ...


class GoogleSheet:
    """Class representing a 'big' sheet with multiple subsheets."""

    def __init__(self, gspread_client: gspread.client.Client, spreadsheet_url: str):
        """
        Args:
            gspread_client: gspread client
            spreadsheet_url: URL of the spreadsheet
        """
        self._gc = gspread_client
        self._sheet = self._gc.open_by_url(spreadsheet_url)
        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet_id = compute_google_resource_id_from_url(spreadsheet_url)

    def _get_subsheets(self) -> list[gspread.Worksheet]:
        return self._sheet.worksheets()

    def get_subsheet_names(self) -> list[str]:
        return [subsheet.title for subsheet in self._get_subsheets()]

    def get_subsheet(self, subsheet_name: str) -> "GoogleSubSheet":
        gspread_subsheet = self._sheet.worksheet(subsheet_name)
        subsheet = GoogleSubSheet(gspread_subsheet, self.spreadsheet_id, subsheet_name)
        return subsheet

    @classmethod
    def from_creds_file(
        cls, creds_path: PathType, spreadsheet_url: str
    ) -> "GoogleSheet":
        gspread_client = gspread.oauth(credentials_filename=creds_path)
        return cls(gspread_client, spreadsheet_url)


class GoogleSubSheet(Sheet):
    def __init__(
        self,
        gspread_worksheet: gspread.Worksheet,
        spreadsheet_id: str,
        spreadsheet_name: str,
    ):
        self._subsheet = gspread_worksheet
        self.spreadsheet_id = spreadsheet_id
        self.name = spreadsheet_name
        self._df = self._to_df()

    @classmethod
    def from_creds_file(
        cls, creds_path: PathType, spreadsheet_url: str, subsheet_name: str
    ) -> "GoogleSubSheet":
        gspread_client = gspread.oauth(credentials_filename=creds_path)
        sheet = GoogleSheet(gspread_client, spreadsheet_url)
        return sheet.get_subsheet(subsheet_name)

    def _find_cells(self, query: str) -> list[gspread.Cell]:
        return self._subsheet.findall(query)

    def _to_df(self) -> pd.DataFrame:
        return pd.DataFrame(self._subsheet.get_all_records())

    def to_df(self) -> pd.DataFrame:
        return self._df

    @property
    def columns(self) -> list[str]:
        return self.to_df().columns

    def write_col(self, col_name: str, col_values: list) -> None:
        col_header_cells = self._find_cells(col_name)
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

        self._subsheet.update(update_range, update_values)
