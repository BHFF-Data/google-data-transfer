import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow
from mentoring_reports_src.commons import PathType


def authenticate_google_api(
    creds_path: PathType, creds_token_path: PathType, scopes: list[str]
) -> Credentials:
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(creds_token_path):
        creds = Credentials.from_authorized_user_file(creds_token_path, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(creds_token_path, "w") as token:
            token.write(creds.to_json())
    return creds
