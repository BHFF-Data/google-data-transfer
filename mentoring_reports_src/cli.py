import gin
import typer
from mentoring_reports_src.controller import download_responses


def main(form_url: str, sheet_url: str, sheet_name: str):
    form_id = form_url.split("/")[-2]
    sheet_id = sheet_url.split("/")[-2]
    sheet_name = sheet_name.replace("_", " ")
    download_responses(form_id, sheet_id, sheet_name)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(main)
