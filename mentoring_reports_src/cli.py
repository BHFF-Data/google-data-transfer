import gin
import typer
from mentoring_reports_src.controller import main


def cli_main(form_url: str, sheet_url: str, sheet_name: str):
    sheet_name = sheet_name.replace("_", " ")  # typer can't accept strings with a space
    main(form_url, sheet_url, sheet_name)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(cli_main)
