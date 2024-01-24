# tutorial
import streamlit as st

from oauth2client.service_account import ServiceAccountCredentials

service_account_path = "./secrets/form_service_account.json"
scopes = (
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly"
)
form_url = "https://docs.google.com/forms/d/1Yal1J9Tgg1Men5MYdD3eT7kjCYaXZhOsuoYSpQU1MU4/edit"

from apiclient import discovery
from httplib2 import Http

SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


def authenticate():
    '''
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        filename=service_account_path,
        scopes=scope)
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = service.files().get(fileId="1FAIpQLSfJbSaTWSEDWx8YNCGF01RcH7_Z0lfLdD_Qb8B9Lkb7Amllig").execute()
    print(file_metadata)
    '''

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        keyfile_dict=st.secrets["service_account"], scopes=scopes)
    http = credentials.authorize(Http())

    form_service = discovery.build('forms', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC,
                                   static_discovery=False, )
    form_id = "1ver4nYOU3mrigFg_ly9f2_HwHvdCKmqQLrR5IXZDGaQ"
    form_result = form_service.forms().responses().list(formId=form_id).execute()
    st.write(form_result["responses"][0])

    DISCOVERY_DOC_SHEET = "https://sheets.googleapis.com/$discovery/rest?version=v4"
    sheet_service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=DISCOVERY_DOC_SHEET,
                                    static_discovery=False)

    sheet_id = "1LMKIqFrrP5AFUDJ37SOIRHLAphV3OiCrR9d4C1t92hQ"
    sheet_result = (
        sheet_service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=sheet_id, ranges="A1:C10")
        .execute()
    )
    st.write(sheet_result);


if __name__ == "__main__":
    authenticate()
