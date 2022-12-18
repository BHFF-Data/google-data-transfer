import os
from typing import Union

import gin
from mentoring_reports_src.dao.forms_dao import GoogleFormsApiDAO
from mentoring_reports_src.google_forms_api_connection import \
    GoogleFormsApiConnection


@gin.configurable
def download_responses(form_id: str, forms_datapath: Union[str, os.PathLike]):
    forms_conn = GoogleFormsApiConnection()
    forms_dao = GoogleFormsApiDAO(google_forms_api_conn=forms_conn, forms_id=form_id)

    df = forms_dao.load_form_data()
    save_path = os.path.join(forms_datapath, f"responses_{form_id}.csv")
    df.to_csv(save_path)
    print(f"Saved {form_id} to {save_path}")
