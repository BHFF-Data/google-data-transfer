import pandas as pd

COLUMNS_JOIN_MAP = {
    "First and Last Name": "Mentee Name",
    "First and Last Name Of Your Mentor": "Mentor Name",
}


def match_form_with_sheet(
    form_df: pd.DataFrame,
    sheet_df: pd.DataFrame,
    columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP,
):
    ...
