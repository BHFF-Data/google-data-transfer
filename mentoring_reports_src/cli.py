import gin
import typer
from mentoring_reports_src.controller import show_responses


def main(form_id: str = None):
    if form_id is None:
        show_responses()
    else:
        show_responses(form_id)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(main)
