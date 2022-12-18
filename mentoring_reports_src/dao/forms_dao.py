from abc import ABC, abstractmethod

from mentoring_reports_src.google_forms_api_connection import \
    GoogleFormsApiConnection


class FormsDAO(ABC):
    @abstractmethod
    def read_form_responses(self):
        ...

    # @abstractmethod
    # def save_form_responses(self, save_path: Union[str, os.PathLike]):
    #    ...


class GoogleFormsApiDAO(FormsDAO):
    def __init__(self, google_forms_api_conn: GoogleFormsApiConnection, forms_id: str):
        self.forms_conn = google_forms_api_conn
        self.forms_id = forms_id

    def read_form_responses(self):
        return self.forms_conn.read_form_responses(self.forms_id)
