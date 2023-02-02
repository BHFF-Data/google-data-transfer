from typing import Optional

import gin
import typer
from google_data_transfer.controller import main
from google_data_transfer.transfer_configs.pickler import pickle_config
from google_data_transfer.transfer_configs.transfer_config import make_config_id

app = typer.Typer()


@app.command(name="transfer")
def cli_main(
    form_url: str,
    sheet_url: str,
    sheet_name: str,
    target_col: Optional[str] = typer.Option(None),
    transfer_config: Optional[str] = "Mentoring Reports Default",
):
    transfer_config_id = make_config_id(transfer_config)
    sheet_name = sheet_name.replace("_", " ")  # typer can't accept strings with a space
    if target_col is not None:
        target_col = target_col.replace("_", " ")
    main(form_url, sheet_url, sheet_name, target_col, transfer_config_id)


@app.command()
def pickle(transfer_config: str):
    transfer_config_id = make_config_id(transfer_config)
    pickle_config(transfer_config_id)
    print("Pickled ", transfer_config)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    app()
