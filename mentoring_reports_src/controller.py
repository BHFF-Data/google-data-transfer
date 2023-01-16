import os

import gin
from mentoring_reports_src.commons import PathType
from mentoring_reports_src.data_transfer import compute_target_col
from mentoring_reports_src.google_api.auth import authenticate_google_api
from mentoring_reports_src.google_api.form import Form, GoogleAPIForm
from mentoring_reports_src.google_api.google_connection import GoogleFormsConnection
from mentoring_reports_src.google_api.sheet import GSpreadSheet, Sheet
from mentoring_reports_src.transfer_functions.mentoring_reports import (
    compute_activity_col,
)

COLUMNS_JOIN_MAP = {
    "First and Last Name": "Mentee",
    "Mentor's First and Last Name": "Mentor",
}

TARGET_COL = "Status - July 2023"


@gin.configurable
def save_google_data(
    form: Form,
    sheet: Sheet,
    forms_save_datapath: PathType = None,
    sheets_save_datapath: PathType = None,
) -> None:
    sheet_df = sheet.to_df()
    form_df = form.to_df()

    if sheets_save_datapath is not None:
        sheets_save_path = os.path.join(
            sheets_save_datapath, f"{sheet.spreadsheet_id}_{sheet.name}.csv"
        )
        sheet_df.to_csv(sheets_save_path)
        print(f"Saved {sheet.spreadsheet_id}, {sheet.name} to {sheets_save_path}")

    if forms_save_datapath is not None:
        save_path = os.path.join(forms_save_datapath, f"{form.id}.csv")
        form_df.to_csv(save_path)
        print(f"Saved {form.id} to {save_path}")


@gin.configurable
def main(
    form_url: str,
    sheet_url: str,
    sheet_name: str,
    secrets_path: PathType,
    save_data: bool = True,
):
    creds_path = secrets_path + "/credentials.json"
    sheet = GSpreadSheet(sheet_url, sheet_name, creds_path)

    creds = authenticate_google_api()
    forms_conn = GoogleFormsConnection(creds)
    form = GoogleAPIForm(form_url, forms_conn)

    transfer_form_responses_to_sheet(form, sheet)
    print("Data transfer successful.")
    if save_data:
        save_google_data(form, sheet)


def transfer_form_responses_to_sheet(
    form: Form,
    sheet: Sheet,
    target_col: str = TARGET_COL,
    columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP,
    transfer_function: callable = compute_activity_col,
) -> None:
    form_df = form.to_df()
    sheet_df = sheet.to_df()
    new_col = compute_target_col(form_df, sheet_df, transfer_function, columns_join_map)
    sheet.write_col(target_col, new_col)
