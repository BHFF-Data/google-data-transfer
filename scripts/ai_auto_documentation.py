import os
from pathlib import Path

KEY_PATH = "../secrets/openai-api-key.txt"

ROOT_SRC = Path("../google_data_transfer/")
CHILD_SRCS = ["google_api", "transfer_configs"]

COMMAND = "docstring_gen"

with open(KEY_PATH, "r") as f:
    openai_api_key = f.read()
os.environ["OPENAI_API_KEY"] = openai_api_key

child_srcs = CHILD_SRCS + [""]
for child_src in child_srcs:
    child_path = ROOT_SRC / child_src
    src_files = os.listdir(child_path)
    src_file_paths = [child_path / file for file in src_files]
    src_file_paths = [path for path in src_file_paths if path.suffix == ".py"]
    for path in src_file_paths:
        command = COMMAND + " " + str(path)
        os.system(command)
