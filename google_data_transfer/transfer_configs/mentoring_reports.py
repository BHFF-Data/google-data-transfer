import os

import pandas as pd
from google_data_transfer.commons import PathType
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

COLUMNS_JOIN_MAP = {
    "First and Last Name": "Mentee",
    "Mentor's First and Last Name": "Mentor",
}
TARGET_COL = "Status - January 2023"
DEFAULT_NAME = "Mentoring Reports Default"


def compute_activity_col(
    form_df: pd.DataFrame,
    activity_question: str = ACTIVITY_QUESTION,
    activity_response_map: dict[str:str] = ACTIVITY_MAP,
    inactivity_question: str = INACTIVITY_REASON_QUESTION,
    inactivity_response_map: dict[str:str] = INACTIVITY_MAP,
    inactivity_value: str = INACTIVITY_VALUE,
    columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP,
) -> pd.DataFrame:
    df = form_df
    df[activity_question] = df[activity_question].replace(activity_response_map)

    if inactivity_question in form_df.columns:
        df[inactivity_question] = df[inactivity_question].replace(
            inactivity_response_map
        )
        df.loc[df[activity_question] == inactivity_value, activity_question] = df.loc[
            df[activity_question] == inactivity_value, inactivity_question
        ]

    form_match_cols = list(columns_join_map.keys())
    form_cols = form_match_cols + [activity_question]
    df = df[form_cols]
    df.rename(columns={activity_question: "target"}, inplace=True)
    return df


def pickle_mentoring_reports(transfer_configs_path: PathType = "./config/transfer/"):
    default_mr = TransferConfig(
        COLUMNS_JOIN_MAP, TARGET_COL, DEFAULT_NAME, compute_activity_col
    )
    os.makedirs(transfer_configs_path, exist_ok=True)
    default_mr.to_pickle(transfer_configs_path)
