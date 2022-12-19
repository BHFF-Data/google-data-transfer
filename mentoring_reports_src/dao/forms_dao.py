from abc import ABC, abstractmethod

import pandas as pd
from mentoring_reports_src.google_api.google_connection import GoogleFormsConnection


class FormsDAO(ABC):
    @abstractmethod
    def load_form_data(self) -> pd.DataFrame:
        ...


class GoogleFormsApiDAO(FormsDAO):
    def __init__(self, forms_id: str, google_forms_conn: GoogleFormsConnection):
        self.forms_conn = google_forms_conn
        self.forms_id = forms_id

    def _read_form_raw_data(self) -> dict[str, dict]:
        raw_data = {
            "contents": self.forms_conn.fetch_form_contents_metadata(self.forms_id),
            "responses": self.forms_conn.fetch_form_responses(self.forms_id),
        }
        return raw_data

    def _get_question_text(self, raw_form_contents: dict, question_id: str) -> str:
        for item in raw_form_contents["items"]:
            if "questionItem" not in item:
                continue
            question_text = item["title"]
            question_dict = item["questionItem"]["question"]
            cur_question_id = question_dict["questionId"]
            if cur_question_id == question_id:
                return question_text
        raise ValueError(f"Question id {question_id} not found in form contents")

    def _join_questions_and_responses(
        self, raw_form_data: dict
    ) -> list[dict[str, str]]:
        records: list[dict[str, str]] = []

        contents = raw_form_data["contents"]
        responses = list(raw_form_data["responses"].values())
        if len(responses) > 1:
            raise NotImplementedError("Unexpected number of items in responses")
        responses = responses[0]
        for response in responses:
            cur_record: dict[str, str] = {}
            for answer in response["answers"].values():
                # TODO: what if it isn't a text answer? line below will raise an exception
                #       probably will have to fetch answer type from question id, along with question text
                text_answers = answer["textAnswers"]["answers"]
                # TODO: what if there are more answers in the list? line below will raise an exception
                if len(text_answers) > 1:
                    raise NotImplementedError("Unexpected number of answers")
                text_answer = text_answers[0]

                answer_text = text_answer["value"]
                question_id = answer["questionId"]
                question_text = self._get_question_text(contents, question_id)
                cur_record[question_text] = answer_text
            records.append(cur_record)
        return records

    def load_form_data(self) -> pd.DataFrame:
        raw_data = self._read_form_raw_data()
        form_data_records = self._join_questions_and_responses(raw_data)
        df = pd.DataFrame.from_records(form_data_records)
        return df
