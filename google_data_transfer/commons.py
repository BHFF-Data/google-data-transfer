import json
import os
import pathlib
from typing import Union


def compute_google_resource_id_from_url(url: str) -> str:
    return url.split("/")[-2]


PathType = Union[str, pathlib.Path]

CREDS_PATH = "./secrets/credentials.json"
CREDS_TOKEN_PATH = "./secrets/token.json"
FORMS_DIR = "./data/forms"
SHEETS_DIR = "./data/sheets"

FORM_RESPONDENT_EMAIL_COL = "__email"
