import pandas as pd
from fuzzywuzzy import fuzz
import warnings
from mentoring_reports_src.transfer_functions.mentoring_reports import compute_activity_col

COLUMNS_JOIN_MAP = {
    "First and Last Name": "Mentee",
    "Mentor's First and Last Name": "Mentor",
}

STRING_REPLACE_MAP = {
    'č': 'c',
    'ć': 'c',
    'š': 's',
    'ž': 'z',
    'đ': 'd',
    ' ': '',
}

TARGET_COL = "Status - July 2023"


def preprocess_string(s: str):
    s = s.lower()
    for old, new in STRING_REPLACE_MAP.items():
        s = s.replace(old, new)
    return s


def match_strings(s1: str, s2: str, string_metric: callable = fuzz.ratio) -> float:
    s1 = preprocess_string(s1)
    s2 = preprocess_string(s2)
    string_distance = string_metric(s1, s2)
    return string_distance


def match_form_with_sheet(
        form_df: pd.DataFrame,
        sheet_df: pd.DataFrame,
        columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP,
) -> dict[tuple:tuple]:
    matched_row_map = {}
    form_cols = columns_join_map.keys()
    sheet_cols = columns_join_map.values()
    for form_row in form_df[form_cols].values:
        max_score = 0
        max_score_sheet_row = None
        for sheet_row in sheet_df[sheet_cols].values:
            total_score = 0
            # Calculate string similarity metric for every column, add to total score
            for form_val, sheet_val in zip(form_row, sheet_row):
                cur_match = match_strings(form_val, sheet_val)
                total_score += cur_match
            # If the score is max, match rows
            if total_score >= max_score:
                max_score = total_score
                max_score_sheet_row = sheet_row
        if max_score < 90:
            warnings.warn(f"Weak match between {form_row} : {max_score_sheet_row}")
        matched_row_map[tuple(form_row)] = tuple(max_score_sheet_row)
    return matched_row_map


def compute_target_col(form_df: pd.DataFrame,
                       sheet_df: pd.DataFrame,
                       transfer_function: callable = compute_activity_col,
                       columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP) -> list:
    form_idx_cols = columns_join_map.keys()
    sheet_idx_cols = columns_join_map.values()
    row_match = match_form_with_sheet(form_df, sheet_df, columns_join_map)
    new_col_df = transfer_function(form_df, columns_join_map)
    new_col = []
    sheet_idx_target_map = {}
    # TODO: change order in match_form_with_sheet, and remove redundant for loop below
    for _, form_row in new_col_df.iterrows():
        form_idx = form_row[form_idx_cols].values
        sheet_idx = row_match[tuple(form_idx)]
        sheet_idx_target_map[sheet_idx] = form_row.target
    for sheet_row in sheet_df[sheet_idx_cols].values:
        new_col_entry = sheet_idx_target_map.get(tuple(sheet_row))
        if new_col_entry is None:
            new_col_entry = "Unknown"
        new_col.append(new_col_entry)
    return new_col


def transfer_data(form_df: pd.DataFrame,
                  sheet_df: pd.DataFrame,
                  transfer_function: callable = compute_activity_col,
                  columns_join_map: dict[str:str] = COLUMNS_JOIN_MAP) -> pd.DataFrame:
    new_col = compute_target_col(form_df, sheet_df, transfer_function, columns_join_map)
    sheet_df[TARGET_COL] = new_col
    return sheet_df
