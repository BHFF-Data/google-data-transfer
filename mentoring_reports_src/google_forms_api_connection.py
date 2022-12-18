import os.path
from typing import Union

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import gin
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


@gin.configurable
class GoogleFormsApiConnection:
    def __init__(self, secrets_dir: Union[str, os.PathLike], scopes: list[str]):
        self.token_path = os.path.join(secrets_dir, "token.json")
        self.creds_path = os.path.join(secrets_dir, "credentials.json")
        self.scopes = scopes
        self.__authenticate()

    def __authenticate(self) -> None:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_path, self.scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())
        # TODO: handle case when form is new and token needs to be regenerated
        self.service = build("forms", "v1", credentials=creds)

    def fetch_form_responses(self, form_id: str) -> dict:
        result = self.service.forms().responses().list(formId=form_id).execute()
        return result

    def fetch_form_contents_metadata(self, form_id: str) -> dict:
        result = self.service.forms().get(formId=form_id).execute()
        return result
