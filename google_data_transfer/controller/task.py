import logging
import os
from typing import Optional

from google_data_transfer.commons import PathType
from google_data_transfer.controller.data_transfer import compute_target_col
from google_data_transfer.google_api.form import Form
from google_data_transfer.google_api.sheet import GoogleSpreadSheet, Worksheet
from google_data_transfer.transfer_configs.transfer_config import TransferConfig

logger = logging.getLogger(__name__)


def transfer_form_responses_to_worksheet(
    form: Form,
    sheet: GoogleSpreadSheet,
    worksheet: Worksheet,
    transfer_config: TransferConfig,
) -> None:
    new_col = compute_target_col(form, sheet, worksheet, transfer_config)
    worksheet.write_col(transfer_config.target_col, new_col)


def save_google_data(
    form: Form,
    sheet: Worksheet,
    form_save_path: Optional[PathType] = None,
    sheet_save_path: Optional[PathType] = None,
) -> None:
    sheet_df = sheet.to_df()
    form_df = form.to_df()

    if sheet_save_path is not None:
        os.makedirs(sheet_save_path, exist_ok=True)
        sheets_save_path = os.path.join(
            sheet_save_path, f"{sheet.spreadsheet_id}_{sheet.name}.csv"
        )
        sheet_df.to_csv(sheets_save_path)
        logger.info(f"Saved {sheet.spreadsheet_id}, {sheet.name} to {sheets_save_path}")

    if form_save_path is not None:
        os.makedirs(form_save_path, exist_ok=True)
        save_path = os.path.join(form_save_path, f"{form.id}.csv")
        form_df.to_csv(save_path)
        logger.info(f"Saved {form.id} to {save_path}")
