import json
import os
from typing import Union


def jprint(dic):
    print(json.dumps(dic, indent=2))


# TODO: handle all path manipulations with pathlib
PathType = Union[str, os.PathLike]
