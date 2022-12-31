import json
import os
from typing import Union


def jprint(dic):
    print(json.dumps(dic, indent=2))


PathType = Union[str, os.PathLike]
