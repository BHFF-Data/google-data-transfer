import pandas as pd
from mentoring_reports_src.dao.forms_dao import GoogleFormsApiDAO
from mentoring_reports_src.dao.google_dao import GoogleDAO
from mentoring_reports_src.dao.sheets_dao import GoogleSheetsApiDAO
from mentoring_reports_src.google_api.google_connection import (
    GoogleFormsConnection,
    GoogleSheetsConnection,
)


class GoogleAPIDao(GoogleDAO):
    def __init__(
        self,
        forms_conn: GoogleFormsConnection = None,
        sheets_con: GoogleSheetsConnection = None,
    ):
        self.forms_conn = forms_conn
        self.sheets_conn = sheets_con

    def load_form_data(self, form_id: str) -> pd.DataFrame:
        form_dao = GoogleFormsApiDAO(form_id, self.forms_conn)
        return form_dao.load_form_data()

    def load_sheet_data(self, sheet_id: str, sheet_name: str) -> pd.DataFrame:
        sheet_dao = GoogleSheetsApiDAO(sheet_id, sheet_name, self.sheets_conn)
        return sheet_dao.load_sheet_data()
