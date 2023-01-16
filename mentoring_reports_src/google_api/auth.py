import os.path
from typing import Union

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import gin
from google_auth_oauthlib.flow import InstalledAppFlow


@gin.configurable
def authenticate_google_api(
    secrets_dir: Union[str, os.PathLike], scopes: list[str]
) -> Credentials:
    token_path = os.path.join(secrets_dir, "token.json")
    creds_path = os.path.join(secrets_dir, "credentials.json")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds
