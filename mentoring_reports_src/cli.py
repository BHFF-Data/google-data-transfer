import gin
import typer
from mentoring_reports_src.controller import load_google_data
from mentoring_reports_src.data_transfer import match_form_with_sheet


def parse_args(form_url: str, sheet_url: str, sheet_name: str):
    form_id = form_url.split("/")[-2]
    sheet_id = sheet_url.split("/")[-2]
    sheet_name = sheet_name.replace("_", " ")
    return form_id, sheet_id, sheet_name


def main(form_url: str, sheet_url: str, sheet_name: str):
    form_id, sheet_id, sheet_name = parse_args(form_url, sheet_url, sheet_name)
    form_df, sheet_df = load_google_data(form_id, sheet_id, sheet_name)
    print("Connected to Google Api")
    res = match_form_with_sheet(form_df, sheet_df)
    print(res)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(main)
