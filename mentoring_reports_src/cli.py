import gin
import typer
from mentoring_reports_src.controller import connect_to_google_api, save_google_data
from mentoring_reports_src.dao.file_system_dao import FileDAO
from mentoring_reports_src.dao.google_api_dao import GoogleAPIDao
from mentoring_reports_src.data_transfer import match_form_with_sheet


def parse_args(form_url: str, sheet_url: str, sheet_name: str):
    form_id = form_url.split("/")[-2]
    sheet_id = sheet_url.split("/")[-2]
    sheet_name = sheet_name.replace("_", " ")
    return form_id, sheet_id, sheet_name


def main(form_url: str, sheet_url: str, sheet_name: str, local: bool = False):
    form_id, sheet_id, sheet_name = parse_args(form_url, sheet_url, sheet_name)
    if local:
        dao = FileDAO()
    else:
        forms_conn, sheets_conn = connect_to_google_api()
        dao = GoogleAPIDao(forms_conn, sheets_conn)
    form_df, sheet_df = save_google_data(form_id, sheet_id, sheet_name, dao)
    print(form_df)
    print(sheet_df)
    # print("Connected to Google Api")
    # res = match_form_with_sheet(form_df, sheet_df)
    # print(res)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(main)
