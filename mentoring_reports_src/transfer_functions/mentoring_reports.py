import pandas as pd

ACTIVITY_QUESTION = "Have you made the inital contact with your mentor?"
ACTIVITY_MAP = {"Yes": "Active", "No": "Inactive"}


def compute_activity_col(
    form_df: pd.DataFrame, columns_join_map: dict[str:str]
) -> pd.DataFrame:
    form_match_cols = list(columns_join_map.keys())
    form_cols = form_match_cols + [ACTIVITY_QUESTION]
    df = form_df[form_cols]
    df[ACTIVITY_QUESTION] = df[ACTIVITY_QUESTION].replace(ACTIVITY_MAP)
    df.rename(columns={ACTIVITY_QUESTION: "target"}, inplace=True)
    return df
