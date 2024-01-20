import logging

import pandas as pd

from google_data_transfer.google_api.form import Form
from google_data_transfer.google_api.sheet import GoogleSpreadSheet, Worksheet
from google_data_transfer.transfer_configs.transfer_config import TransferConfig

logger = logging.getLogger(__name__)


def compute_target_col(
    form: Form,
    sheet: GoogleSpreadSheet,
    worksheet: Worksheet,
    transfer_config: TransferConfig,
) -> list[str]:
    form_df = form.to_df()
    sheet_df = worksheet.to_df()
    # Which form questions were matched to which sheet columns
    sheet_to_form_row_match_map = transfer_config.match_rows(form, sheet, worksheet)
    # Compute
    new_col_df = transfer_config.transfer(form_df)
    #{("Abdulah Kadiric", "Mujo Haso") : None, ("Ajla Korman", "Lartida Nuhanovic"): "korman.ajla115@gmail.com" ...
    #   }  # TODO : ovako izgleda output za testnu formu!
    # Replace form row id values with sheet row id values
    form_id_cols = list(transfer_config.match_col_form_name_to_sheet_name_map.keys())
    form_to_sheet_row_match_map = {v: k for k, v in sheet_to_form_row_match_map.items()}
    new_col_df["match_col"] = new_col_df[form_id_cols].astype(str).agg("".join, axis=1)
    replace_dict = {
        "".join(k): "".join(v)
        for k, v in form_to_sheet_row_match_map.items()
        if k is not None
    }
    new_col_df = new_col_df.replace({"match_col": replace_dict})
    # Join new column with sheet
    sheet_id_cols = list(transfer_config.match_col_form_name_to_sheet_name_map.values())
    sheet_df["match_col"] = sheet_df[sheet_id_cols].astype(str).agg("".join, axis=1)
    df = pd.merge(sheet_df, new_col_df, on="match_col", how="left")
    df = df.fillna(transfer_config.missing_fill_value)
    return df.target.values.tolist()
