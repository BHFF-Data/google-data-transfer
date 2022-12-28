import os.path

import pandas as pd
from mentoring_reports_src.commons import PathType
from mentoring_reports_src.dao.google_dao import GoogleDAO


class FileDAO(GoogleDAO):
    def __init__(self, forms_path: PathType, sheets_path: PathType):
        self.forms_path = forms_path
        self.sheets_path = sheets_path

    def load_form_data(self, form_id: str) -> pd.DataFrame:
        form_path = os.path.join(self.forms_path, form_id + ".csv")
        df = pd.read_csv(form_path, index_col=0)
        return df

    def load_sheet_data(self, sheet_id: str, sheet_name: str) -> pd.DataFrame:
        sheet_path = os.path.join(
            self.sheets_path, sheet_id + "_" + sheet_name + ".csv"
        )
        df = pd.read_csv(sheet_path, index_col=0)
        return df
