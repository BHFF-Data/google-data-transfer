from typing import Optional

import gin

from google_data_transfer.commons import CREDS_PATH, CREDS_TOKEN_PATH
from google_data_transfer.controller.task import transfer_form_responses_to_sheet
from google_data_transfer.google_api.form import GoogleForm
from google_data_transfer.google_api.sheet import GoogleSheet, GoogleSubSheet
from google_data_transfer.transfer_configs.mentoring_reports import (
    MentoringReportsTransferConfig,
)
from google_data_transfer.transfer_configs.transfer_config import TransferConfig


@gin.configurable
class WebApp:
    _google_api_scopes: tuple
    _form: Optional[GoogleForm] = None
    _sheet: Optional[GoogleSheet] = None
    _subsheet: Optional[GoogleSubSheet] = None
    _transfer_config: Optional[TransferConfig] = None

    def __init__(
        self, google_api_scopes: tuple, transfer_config: Optional[TransferConfig] = None
    ):
        self._google_api_scopes = google_api_scopes
        if transfer_config is None:
            transfer_config = MentoringReportsTransferConfig()
        self._transfer_config = transfer_config

    def init_form(self, form_url: str):
        self._form = GoogleForm.from_creds_file(
            CREDS_PATH, CREDS_TOKEN_PATH, self._google_api_scopes, form_url
        )

    def init_sheet(self, sheet_url: str):
        self._sheet = GoogleSheet.from_creds_file(CREDS_PATH, sheet_url)

    def init_subsheet(self, sheet_name: str):
        self._subsheet = self._sheet.get_subsheet(sheet_name)

    def get_subsheet_names(self) -> list[str]:
        return self._sheet.get_subsheet_names()

    def get_sheet_cols(self) -> list[str]:
        return self._subsheet.columns

    def transfer(self, target_col: str):
        self._transfer_config.target_col = target_col
        transfer_form_responses_to_sheet(
            self._form, self._subsheet, self._transfer_config
        )
