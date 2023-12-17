import logging

import gin

from google_data_transfer.commons import (
    CREDS_PATH,
    CREDS_TOKEN_PATH,
    FORMS_DIR,
    SHEETS_DIR,
    PathType,
)
from google_data_transfer.controller.task import (
    save_google_data,
    transfer_form_responses_to_sheet,
)
from google_data_transfer.google_api.form import GoogleAPIForm
from google_data_transfer.google_api.sheet import GSpreadSheet
from google_data_transfer.transfer_configs.mentoring_reports import (
    MentoringReportsTransferConfig,
)

logger = logging.getLogger(__name__)


@gin.configurable
def process_mentoring_reports(
    form_url: str,
    sheet_url: str,
    sheet_name: str,
    target_col: str,
    google_api_scopes: list[str],
    creds_path: PathType = CREDS_PATH,
    creds_token_path: PathType = CREDS_TOKEN_PATH,
    form_save_path: PathType = FORMS_DIR,
    sheet_save_path: PathType = SHEETS_DIR,
    save_data: bool = True,
):
    """Main function to transfer data from a Google Form to a Google Sheet.

    Args:
        form_url: URL of the Google Form
        sheet_url: URL of the Google Sheet
        sheet_name: Name of the Google Sheet
        target_col: Target column in the Google Sheet
        creds_path: Path to the credentials
        creds_token_path: Path to the credentials token
        google_api_scopes: List of Google API scopes
        save_data: Whether to save the data
        sheet_save_path: Path where the sheet will be saved
        form_save_path: Path where the form will be saved

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """
    sheet = GSpreadSheet.from_creds_file(creds_path, sheet_url, sheet_name)
    form = GoogleAPIForm.from_creds_file(
        creds_path, creds_token_path, google_api_scopes, form_url
    )
    transfer_config = MentoringReportsTransferConfig()

    transfer_form_responses_to_sheet(form, sheet, target_col, transfer_config)
    logger.info("Data transfer successful.")

    if save_data:
        save_google_data(form, sheet, form_save_path, sheet_save_path)