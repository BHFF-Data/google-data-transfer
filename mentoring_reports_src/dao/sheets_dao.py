from abc import ABC, abstractmethod

import pandas as pd
from mentoring_reports_src.google_api.google_connection import GoogleSheetsConnection


class SheetsDAO(ABC):
    @abstractmethod
    def load_sheet_data(self) -> pd.DataFrame:
        ...


class GoogleSheetsApiDAO(SheetsDAO):
    def __init__(
        self, sheet_id: str, sheet_name: str, google_sheets_conn: GoogleSheetsConnection
    ):
        self.sheets_conn = google_sheets_conn
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name

    def _read_sheet_raw_data(self) -> list[list]:
        raw_data = self.sheets_conn.fetch_sheet_contents(self.sheet_id, self.sheet_name)
        return raw_data

    def load_sheet_data(self) -> pd.DataFrame:
        raw_data = self._read_sheet_raw_data()
        columns = raw_data.pop(0)
        df = pd.DataFrame(raw_data, columns=columns)
        return df
