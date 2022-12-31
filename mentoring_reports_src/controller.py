import os

import gin
import pandas as pd
from mentoring_reports_src.commons import PathType
from mentoring_reports_src.dao.google_dao import GoogleDAO
from mentoring_reports_src.data_transfer import compute_target_col
from mentoring_reports_src.google_api.auth import authenticate_google_api
from mentoring_reports_src.google_api.google_connection import (
    GoogleFormsConnection,
    GoogleSheetsConnection,
)
from mentoring_reports_src.transfer_functions.mentoring_reports import (
    compute_activity_col,
)

COLUMNS_JOIN_MAP = {
    "First and Last Name": "Mentee",
    "Mentor's First and Last Name": "Mentor",
}

TARGET_COL = "Status - July 2023"


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


def transfer_form_responses_to_sheet(
    form_df: pd.DataFrame,
    sheet_df: pd.DataFrame,
    target_col: str = TARGET_COL,
    columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP,
    transfer_function: callable = compute_activity_col,
) -> pd.DataFrame:
    new_col = compute_target_col(form_df, sheet_df, transfer_function, columns_join_map)
    sheet_df[target_col] = new_col
    return sheet_df
