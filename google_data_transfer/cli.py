import logging
from typing import Optional

import fire
import gin

from google_data_transfer.controller.cli import process_mentoring_reports

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def mentoring_reports(
    form_url: str,
    sheet_url: str,
    sheet_name: str,
    target_col: Optional[str] = None,
):
    process_mentoring_reports(form_url, sheet_url, sheet_name, target_col)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    fire.Fire(mentoring_reports)
