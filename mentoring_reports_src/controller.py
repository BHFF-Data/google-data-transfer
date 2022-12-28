import os

import gin
import pandas as pd
from mentoring_reports_src.commons import PathType
from mentoring_reports_src.dao.google_dao import GoogleDAO
from mentoring_reports_src.google_api.auth import authenticate_google_api
from mentoring_reports_src.google_api.google_connection import (
    GoogleFormsConnection,
    GoogleSheetsConnection,
)


def connect_to_google_api():
    creds = authenticate_google_api()
    forms_conn = GoogleFormsConnection(creds)
    sheets_conn = GoogleSheetsConnection(creds)
    return forms_conn, sheets_conn


@gin.configurable
def save_google_data(
    form_id: str,
    sheet_id: str,
    sheet_name: str,
    dao: GoogleDAO,
    forms_save_datapath: PathType = None,
    sheets_save_datapath: PathType = None,
) -> (pd.DataFrame, pd.DataFrame):
    sheets_df = dao.load_sheet_data(sheet_id, sheet_name)

    if sheets_save_datapath is not None:
        sheets_save_path = os.path.join(
            sheets_save_datapath, f"{sheet_id}_{sheet_name}.csv"
        )
        sheets_df.to_csv(sheets_save_path)
        print(f"Saved {sheet_id}, {sheet_name} to {sheets_save_path}")

    forms_df = dao.load_form_data(form_id)
    if forms_save_datapath is not None:
        save_path = os.path.join(forms_save_datapath, f"{form_id}.csv")
        forms_df.to_csv(save_path)
        print(f"Saved {form_id} to {save_path}")

    return forms_df, sheets_df
