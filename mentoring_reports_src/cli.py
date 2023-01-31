from typing import Optional

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
    target_col: Optional[str] = typer.Option(None),
    transfer_config: Optional[str] = "Mentoring Reports Default",
):
    # TODO: ADD CLI MODE FOR PICKLING CONFIGS! IT SHOULD HAPPEN ONLY THE FIRST TIME THE CONFIG IS USED
    pickle_mentoring_reports()

    transfer_config_id = make_config_id(transfer_config)
    sheet_name = sheet_name.replace("_", " ")  # typer can't accept strings with a space
    if target_col is not None:
        target_col = target_col.replace("_", " ")
    main(form_url, sheet_url, sheet_name, target_col, transfer_config_id)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(cli_main)
