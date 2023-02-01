from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build


class GoogleConnection:
    def __init__(self, creds: Credentials):
        self.creds = creds


class GoogleFormsConnection(GoogleConnection):
    def __init__(self, creds: Credentials):
        super().__init__(creds)
        self.service = build("forms", "v1", credentials=self.creds)

    def fetch_form_responses(self, form_id: str) -> dict:
        result = self.service.forms().responses().list(formId=form_id).execute()
        return result

    def fetch_form_contents_metadata(self, form_id: str) -> dict:
        result = self.service.forms().get(formId=form_id).execute()
        return result


class GoogleSheetsConnection(GoogleConnection):
    def __init__(self, creds: Credentials):
        super().__init__(creds)
        self.service = build("sheets", "v4", credentials=self.creds)

    def fetch_sheet_contents(self, sheet_id: str, sheet_name: str) -> list[list]:
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
        values = result.get("values", [])
        return values

    def write_sheet_row(self):
        ...
