from abc import ABC, abstractmethod

import pandas as pd
from mentoring_reports_src.google_forms_api_connection import \
    GoogleFormsApiConnection


class FormsDAO(ABC):
    @abstractmethod
    def load_form_data(self) -> pd.DataFrame:
        ...


class GoogleFormsApiDAO(FormsDAO):
    def __init__(self, google_forms_api_conn: GoogleFormsApiConnection, forms_id: str):
        self.forms_conn = google_forms_api_conn
        self.forms_id = forms_id

    def _read_form_raw_data(self) -> dict:
        raw_data = {
            "contents_and_metadata": self.forms_conn.fetch_form_contents_metadata(
                self.forms_id
            ),
            "responses": self.forms_conn.fetch_form_responses(self.forms_id),
        }
        return raw_data

    def _join_questions_and_responses(self, raw_form_data: dict):
        joined_dict = {}
        for item in raw_form_data["contents_and_metadata"]["items"]:
            if "questionItem" not in item:
                raise NotImplementedError("Form item is not a question")
            question_text = item["title"]
            joined_dict[question_text] = []
            question_dict = item["questionItem"]["question"]
            question_id = question_dict["questionId"]

            for response_list in raw_form_data["responses"].values():
                for response in response_list:
                    for answer in response["answers"].values():
                        # TODO what if it isn't a text answer?
                        # TODO what if there are more answers? (idx > 0?)
                        text_answer = answer["textAnswers"]["answers"][0]["value"]
                        if answer["questionId"] == question_id:
                            joined_dict[question_text].append(text_answer)
        return joined_dict

    def load_form_data(self) -> pd.DataFrame:
        raw_data = self._read_form_raw_data()
        form_data_dict = self._join_questions_and_responses(raw_data)
        df = pd.DataFrame.from_dict(form_data_dict, orient="index").transpose()
        return df
