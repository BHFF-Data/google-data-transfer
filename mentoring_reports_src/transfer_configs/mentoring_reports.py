import os

import pandas as pd
from mentoring_reports_src.commons import PathType
from mentoring_reports_src.transfer_configs.transfer_config import TransferConfig

ACTIVITY_QUESTION = "Have you made the inital contact with your mentor?"
ACTIVITY_MAP = {"Yes": "Active", "No": "Inactive"}
COLUMNS_JOIN_MAP = {
    "First and Last Name": "Mentee",
    "Mentor's First and Last Name": "Mentor",
}
TARGET_COL = "Status - July 2023"
DEFAULT_NAME = "Mentoring Reports Default"


def compute_activity_col(
    form_df: pd.DataFrame,
    activity_question: str = ACTIVITY_QUESTION,
    activity_response_map: str = ACTIVITY_MAP,
    columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP,
) -> pd.DataFrame:
    form_match_cols = list(columns_join_map.keys())
    form_cols = form_match_cols + [activity_question]
    df = form_df[form_cols]
    df[activity_question] = df[activity_question].replace(activity_response_map)
    df.rename(columns={activity_question: "target"}, inplace=True)
    return df


def pickle_mentoring_reports(transfer_configs_path: PathType = "./config/transfer/"):
    default_mr = TransferConfig(
        COLUMNS_JOIN_MAP, TARGET_COL, DEFAULT_NAME, compute_activity_col
    )
    os.makedirs(transfer_configs_path, exist_ok=True)
    default_mr.to_pickle(transfer_configs_path)
