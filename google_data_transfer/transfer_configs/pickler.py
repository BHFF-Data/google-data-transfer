"""
In order to be loaded, the pickled file must be pickled inside the entry point file.
This module provides pickling inside of cli.py, based on the config name
"""

from google_data_transfer.transfer_configs.mentoring_reports import (
    pickle_mentoring_reports,
)

ID_FUN_MAP = {"mentoring_reports_default": pickle_mentoring_reports}


def pickle_config(config_id: str, id_fun_map: dict[str:callable] = ID_FUN_MAP) -> None:
    fun = id_fun_map[config_id]
    fun()
