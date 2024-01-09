from typing import Optional

import pandas as pd

from google_data_transfer.google_api.form import Form
from google_data_transfer.google_api.sheet import GoogleSpreadSheet
from google_data_transfer.transfer_configs.transfer_config import TransferConfig

ACTIVITY_QUESTION = "Do you have recommended number of meetings with your mentor?"
INACTIVITY_REASON_QUESTION = (
    "If the answer to the previous question is 'No', please state why"
)

INACTIVITY_VALUE = "Inactive"
ACTIVITY_MAP = {"Yes": "Active", "No": INACTIVITY_VALUE}
INACTIVITY_MAP = {
    "I wasn't available for my mentor": "Inactive due to mentee",
    "My Mentor wasn't available for me": "Inactive due to mentor",
}

MATCH_COL_FORM_NAME_TO_SHEET_NAME_MAP = {
    "First and Last Name": "Mentee",
    "Mentor's First and Last Name": "Mentor",
}
TARGET_COL = "Status - January 2023"
DEFAULT_NAME = "Mentoring Reports Default"
MISSING_FILL_VALUE = "Unknown (report is missing)"




class MentoringReportsTransferConfig(TransferConfig):
    def __init__(
        self,
        match_col_form_name_to_sheet_name_map: Optional[dict[str, str]] = None,
        target_col: Optional[str] = None,
        name: str = DEFAULT_NAME,
        missing_fill_value: str = MISSING_FILL_VALUE,
    ):
        if match_col_form_name_to_sheet_name_map is None:
            match_col_form_name_to_sheet_name_map = (
                MATCH_COL_FORM_NAME_TO_SHEET_NAME_MAP
            )
        if target_col is None:
            self.target_col = TARGET_COL
        super().__init__(match_col_form_name_to_sheet_name_map, target_col, name, missing_fill_value)

    def transfer(
        self,
        form_df: pd.DataFrame,
        activity_question: str = ACTIVITY_QUESTION,
        activity_response_map: Optional[dict[str, str]] = None,
        inactivity_question: str = INACTIVITY_REASON_QUESTION,
        inactivity_response_map: Optional[dict[str, str]] = None,
        inactivity_value: str = INACTIVITY_VALUE,
    ) -> pd.DataFrame:
        """Compute the activity column

        Args:
            form_df: The dataframe
            activity_question: The activity question
            activity_response_map: The activity response map
            inactivity_question: The inactivity question
            inactivity_response_map: The inactivity response map
            inactivity_value: The inactivity value

        Returns:
            The dataframe with the activity column

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        if activity_response_map is None:
            activity_response_map = ACTIVITY_MAP
        if inactivity_response_map is None:
            inactivity_response_map = INACTIVITY_MAP
        df = form_df
        df[activity_question] = df[activity_question].replace(activity_response_map)

        if inactivity_question in form_df.columns:
            df[inactivity_question] = df[inactivity_question].replace(
                inactivity_response_map
            )
            df.loc[
                df[activity_question] == inactivity_value, activity_question
            ] = df.loc[df[activity_question] == inactivity_value, inactivity_question]

        form_match_cols = list(self.match_col_form_name_to_sheet_name_map.keys())
        form_cols = form_match_cols + [activity_question]
        df = df[form_cols]
        df = df.rename(columns={activity_question: "target"})
        return df

    def match_rows(self, form: Form, sheet: GoogleSpreadSheet) -> dict:
        ...
