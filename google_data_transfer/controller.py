import os
from pathlib import Path

import gin
from google_data_transfer.commons import PathType
from google_data_transfer.data_transfer import compute_target_col
from google_data_transfer.google_api.auth import authenticate_google_api
from google_data_transfer.google_api.form import Form, GoogleAPIForm
from google_data_transfer.google_api.google_connection import GoogleFormsConnection
from google_data_transfer.google_api.sheet import GSpreadSheet, Sheet
from google_data_transfer.transfer_configs.transfer_config import TransferConfig


@gin.configurable
def main(
    form_url: str,
    sheet_url: str,
    sheet_name: str,
    target_col: str,
    transfer_config_id: str,
    transfer_configs_path: PathType,
    creds_path: PathType,
    creds_token_path: PathType,
    google_api_scopes: list[str],
    save_data: bool = True,
):
    pickle_config_path = Path(transfer_configs_path) / (transfer_config_id + ".pickle")
    transfer_config = TransferConfig.from_pickle(pickle_config_path)

    sheet = GSpreadSheet(sheet_url, sheet_name, creds_path)

    creds = authenticate_google_api(creds_path, creds_token_path, google_api_scopes)
    forms_conn = GoogleFormsConnection(creds)
    form = GoogleAPIForm(form_url, forms_conn)

    transfer_form_responses_to_sheet(form, sheet, target_col, transfer_config)
    # TODO: add logging
    print("Data transfer successful.")
    if save_data:
        save_google_data(form, sheet)


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
        os.makedirs(sheets_save_datapath, exist_ok=True)
        sheets_save_path = os.path.join(
            sheets_save_datapath, f"{sheet.spreadsheet_id}_{sheet.name}.csv"
        )
        sheet_df.to_csv(sheets_save_path)
        print(f"Saved {sheet.spreadsheet_id}, {sheet.name} to {sheets_save_path}")

    if forms_save_datapath is not None:
        os.makedirs(forms_save_datapath, exist_ok=True)
        save_path = os.path.join(forms_save_datapath, f"{form.id}.csv")
        form_df.to_csv(save_path)
        print(f"Saved {form.id} to {save_path}")


def transfer_form_responses_to_sheet(
    form: Form, sheet: Sheet, target_col: str, transfer_config: TransferConfig
) -> None:
    form_df = form.to_df()
    sheet_df = sheet.to_df()
    new_col = compute_target_col(
        form_df,
        sheet_df,
        transfer_config.transfer_function,
        transfer_config.columns_join_map,
    )
    if target_col is None:
        target_col = transfer_config.target_col
    sheet.write_col(target_col, new_col)
