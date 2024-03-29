from abc import ABC, abstractmethod

import pandas as pd

from google_data_transfer.commons import PathType, compute_google_resource_id_from_url
from google_data_transfer.google_api.auth import authenticate_google_api
from google_data_transfer.google_api.google_client import GoogleFormsClient


class Form(ABC):
    id: str

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        ...


class GoogleForm(Form):
    def __init__(self, form_url: str, google_form_client: GoogleFormsClient):
        self.url = form_url
        self.id = compute_google_resource_id_from_url(form_url)
        self._google_client = google_form_client
        self._contents_metadata = self._read_form_contents_metadata()

    @classmethod
    def from_creds_file(
        cls,
        creds_path: PathType,
        creds_token_path: PathType,
        scopes: tuple[str],
        form_url: str,
    ):
        creds = authenticate_google_api(creds_path, creds_token_path, scopes)
        forms_client = GoogleFormsClient(creds)
        return cls(form_url, forms_client)

    def _read_form_contents_metadata(self) -> dict:
        return self._google_client.fetch_form_contents_metadata(self.id)

    def _read_form_responses(self) -> list:
        return self._google_client.fetch_form_responses(self.id)["responses"]

    def _get_question_text(self, question_id: str) -> str:
        for item in self._contents_metadata["items"]:
            if "questionItem" not in item:
                continue
            question_text = item["title"]
            question_dict = item["questionItem"]["question"]
            cur_question_id = question_dict["questionId"]
            if cur_question_id == question_id:
                return question_text
        raise ValueError(f"Question id {question_id} not found in form contents")

    def to_df(
        self,
    ) -> pd.DataFrame:
        records: list[dict[str, str]] = []
        for response in self._read_form_responses():
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
                question_text = self._get_question_text(question_id)
                cur_record[question_text] = answer_text
            records.append(cur_record)
        df = pd.DataFrame.from_records(records)
        return df
