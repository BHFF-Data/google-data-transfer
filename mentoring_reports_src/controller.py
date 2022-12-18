from mentoring_reports_src.dao.forms_dao import GoogleFormsApiDAO
from mentoring_reports_src.google_forms_api_connection import \
    GoogleFormsApiConnection

FORMS_ID = "1rk03IPnpSQi6W_GFCaARNMyLzF21800ZrktbqzLY1bg"


def show_responses(form_id=FORMS_ID):
    forms_conn = GoogleFormsApiConnection()
    forms_dao = GoogleFormsApiDAO(google_forms_api_conn=forms_conn, forms_id=form_id)
    responses = forms_dao.read_form_responses()
    print(responses)
