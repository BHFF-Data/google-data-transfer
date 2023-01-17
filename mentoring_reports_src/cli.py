import gin
import typer
from mentoring_reports_src.controller import main
from mentoring_reports_src.transfer_configs.mentoring_reports import (
    pickle_mentoring_reports,
)
from mentoring_reports_src.transfer_configs.transfer_config import make_config_id


def cli_main(
    form_url: str,
    sheet_url: str,
    sheet_name: str,
    transfer_config: str = "Mentoring Reports Default",
):
    # TODO: ADD MODE FOR PICKLING CONFIGS!
    pickle_mentoring_reports()

    transfer_config_id = make_config_id(transfer_config)
    sheet_name = sheet_name.replace("_", " ")  # typer can't accept strings with a space
    main(form_url, sheet_url, sheet_name, transfer_config_id)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(cli_main)
