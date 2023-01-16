import warnings

import pandas as pd
from fuzzywuzzy import fuzz

STRING_REPLACE_MAP = {"č": "c", "ć": "c", "š": "s", "ž": "z", "đ": "d", " ": ""}


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
    form_df: pd.DataFrame, sheet_df: pd.DataFrame, columns_join_map: dict[str:str]
) -> dict[tuple:tuple]:
    matched_row_map = {}
    form_cols = columns_join_map.keys()
    sheet_cols = columns_join_map.values()
    for sheet_row in sheet_df[sheet_cols].values:
        max_score = 0
        max_score_form_row = None
        for form_row in form_df[form_cols].values:
            # If already matched
            if tuple(form_row) in matched_row_map.values():
                continue
            total_score = 0
            # Calculate string similarity metric for every column, add to total score
            for form_val, sheet_val in zip(form_row, sheet_row):
                cur_match = match_strings(form_val, sheet_val)
                total_score += cur_match
            # If the score is max, match rows
            if total_score >= max_score:
                max_score = total_score
                max_score_form_row = form_row
        matched_form_row = tuple(max_score_form_row)
        # Allow 10% difference between each string
        # TODO: make the limit configurable. Optionally match each string individually
        if max_score < 90 * len(sheet_cols):
            warnings.warn(
                f"Weak match [{max_score / len(sheet_cols)}%] between {sheet_row} : {max_score_form_row}. This row "
                f"wasn't matched."
            )
            matched_form_row = None
        matched_row_map[tuple(sheet_row)] = matched_form_row
    return matched_row_map


def compute_target_col(
    form_df: pd.DataFrame,
    sheet_df: pd.DataFrame,
    transfer_function: callable,
    columns_join_map: dict[str:str],
) -> list:
    sheet_id_cols = columns_join_map.values()
    # Which form questions were matched to which sheet columns
    row_match_dict = match_form_with_sheet(form_df, sheet_df, columns_join_map)
    # Compute new col from form
    new_col_df = transfer_function(form_df, columns_join_map)
    # Sort new col by position in sheet
    new_col = []
    for sheet_row in sheet_df[sheet_id_cols].values:
        matched_form_row = row_match_dict[tuple(sheet_row)]
        # If no response was found in forms
        if matched_form_row is None:
            new_col.append(
                "Unknown (report is missing)"
            )  # TODO: ADD MESSAGE AS PARAMETER
            continue
        # Get the target which was matched with sheet row
        pandas_subqueries = [
            "`" + form_question + "`" + "==" + '"' + form_answer + '"'
            for form_question, form_answer in zip(
                columns_join_map.keys(), matched_form_row
            )
        ]
        pandas_query = " and ".join(pandas_subqueries)
        df = new_col_df.query(pandas_query)
        target = df.target.values[0]
        new_col.append(target)
    return new_col
