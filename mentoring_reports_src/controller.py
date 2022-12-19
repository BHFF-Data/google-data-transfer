import os
from typing import Union

import gin
from mentoring_reports_src.dao.forms_dao import GoogleFormsApiDAO
from mentoring_reports_src.dao.sheets_dao import GoogleSheetsApiDAO
from mentoring_reports_src.google_api.auth import authenticate_google_api
from mentoring_reports_src.google_api.google_connection import (GoogleFormsConnection,
                                                                GoogleSheetsConnection)


@gin.configurable
def download_responses(
    form_id: str,
    sheet_id: str,
    sheet_name: str,
    forms_datapath: Union[str, os.PathLike],
    sheets_datapath: Union[str, os.PathLike],
) -> None:

    creds = authenticate_google_api()
    forms_conn = GoogleFormsConnection(creds)
    sheets_conn = GoogleSheetsConnection(creds)

    forms_dao = GoogleFormsApiDAO(google_forms_conn=forms_conn, forms_id=form_id)
    sheets_dao = GoogleSheetsApiDAO(
        google_sheets_conn=sheets_conn, sheet_id=sheet_id, sheet_name=sheet_name
    )

    df = sheets_dao.load_sheet_data()
    sheets_save_path = os.path.join(sheets_datapath, f"sheet_{sheet_id}.csv")
    df.to_csv(sheets_save_path)
    print(f"Saved {sheet_id} to {sheets_save_path}")

    df = forms_dao.load_form_data()
    save_path = os.path.join(forms_datapath, f"responses_{form_id}.csv")
    df.to_csv(save_path)
    print(f"Saved {form_id} to {save_path}")
