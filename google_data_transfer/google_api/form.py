from abc import ABC, abstractmethod

import pandas as pd
from google_data_transfer.google_api.google_connection import GoogleFormsConnection


class Form(ABC):
    """A class to represent a form.

    Attributes:
        id: The id of the form

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """

    id: str

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        """!!! note

        Failed to generate docs

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        ...


class GoogleAPIForm(Form):
    """A class to represent a Google Form.

    Attributes:
        url : URL of the form
        id : ID of the form
        _google_conn : GoogleFormsConnection object

    !!! note

        The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
    """

    def __init__(self, form_url: str, google_form_conn: GoogleFormsConnection):
        """
        Args:
            form_url: URL of the Google Form
            google_form_conn: Connection to Google Forms

        Attributes:
            url: URL of the Google Form
            id: ID of the Google Form
            _google_conn: Connection to Google Forms


        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        self.url = form_url
        self.id = form_url.split("/")[-2]
        self._google_conn = google_form_conn

    def _read_form_raw_data(self) -> dict[str, dict]:
        """!!! note

        Failed to generate docs

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        raw_data = {
            "contents": self._google_conn.fetch_form_contents_metadata(self.id),
            "responses": self._google_conn.fetch_form_responses(self.id),
        }
        return raw_data

    def _get_question_text(self, raw_form_contents: dict, question_id: str) -> str:
        """Get the text of a question from a Google Form.

        Args:
            raw_form_contents: The raw contents of a Google Form.
            question_id: The id of the question to get the text of.

        Returns:
            The text of the question.

        Raises:
            ValueError: If the question id is not found in the form contents.

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
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
        """
        Args:
            raw_form_data:

        Returns:
            list[dict[str, str]]:

        Raises:
            NotImplementedError:

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
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

    def to_df(self) -> pd.DataFrame:
        """
        Args:
            self:

        Returns:
            The dataframe

        Raises:
            ValueError: If s1 or s2 is None

        !!! note

            The above docstring is autogenerated by docstring-gen library (https://docstring-gen.airt.ai)
        """
        raw_data = self._read_form_raw_data()
        form_data_records = self._join_questions_and_responses(raw_data)
        df = pd.DataFrame.from_records(form_data_records)
        return df
