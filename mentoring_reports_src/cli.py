import gin
import typer
from mentoring_reports_src.controller import download_responses


def main(form_url: str = None):
    if form_url is None:
        download_responses()
    else:
        form_id = form_url.split("/")[-2]
        download_responses(form_id)


if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    typer.run(main)
