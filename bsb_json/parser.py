"""
JSON parsing module. Built on top of the Python ``json`` module. Adds JSON imports and
references.
"""

import json

import numpy as np
from bsb.config.parsers import ReferenceParser


def _json_iter(obj):  # pragma: nocover
    if isinstance(obj, dict):
        return obj.items()
    elif isinstance(obj, list):
        return iter(obj)
    else:
        return iter(())


def _to_json(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    else:
        raise TypeError(f"Can't encode '{value}' ({type(value)})")


class JsonParser(ReferenceParser):
    """
    Parser plugin class to parse JSON configuration files.
    """

    data_description = "JSON"
    data_extensions = ("json",)
    data_syntax = "json"

    def from_str(self, filename):
        return json.loads(filename)

    def load_content(self, stream):
        return json.load(stream)

    def generate(self, tree, pretty=False):
        if pretty:
            return json.dumps(tree, indent=4, default=_to_json)
        else:
            return json.dumps(tree, default=_to_json)


__plugin__ = JsonParser
