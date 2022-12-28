import os
from typing import Union

import gin
import pandas as pd

from mentoring_reports_src.dao.forms_dao import GoogleFormsApiDAO
from mentoring_reports_src.dao.sheets_dao import GoogleSheetsApiDAO
from mentoring_reports_src.google_api.auth import authenticate_google_api
from mentoring_reports_src.google_api.google_connection import (GoogleFormsConnection,
                                                                GoogleSheetsConnection)


def connect_to_google_api():
    creds = authenticate_google_api()
    forms_conn = GoogleFormsConnection(creds)
    sheets_conn = GoogleSheetsConnection(creds)
    return forms_conn, sheets_conn


@gin.configurable
def load_google_data(
        form_id: str,
        sheet_id: str,
        sheet_name: str,
        forms_save_datapath: Union[str, os.PathLike] = None,
        sheets_save_datapath: Union[str, os.PathLike] = None,
) -> (pd.DataFrame, pd.DataFrame):
    forms_conn, sheets_conn = connect_to_google_api()
    forms_dao = GoogleFormsApiDAO(google_forms_conn=forms_conn, forms_id=form_id)
    sheets_dao = GoogleSheetsApiDAO(
        google_sheets_conn=sheets_conn, sheet_id=sheet_id, sheet_name=sheet_name
    )

    sheets_df = sheets_dao.load_sheet_data()
    if sheets_save_datapath is not None:
        sheets_save_path = os.path.join(sheets_save_datapath, f"sheet_{sheet_id}.csv")
        sheets_df.to_csv(sheets_save_path)
        print(f"Saved {sheet_id} to {sheets_save_path}")

    forms_df = forms_dao.load_form_data()
    if forms_save_datapath is not None:
        save_path = os.path.join(forms_save_datapath, f"responses_{form_id}.csv")
        forms_df.to_csv(save_path)
        print(f"Saved {form_id} to {save_path}")

    return forms_df, sheets_df
