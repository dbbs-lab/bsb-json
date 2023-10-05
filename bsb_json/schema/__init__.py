import json
import typing
from bsb.core import Scaffold
from bsb.config import get_config_attributes


def schema(root):
    schema = object_schema(root)
    schema["title"] = "Configuration"
    schema["description"] = "Automated JSON schema of configuration object"
    return json.dumps(schema)

def object_schema(obj):
    schema = {"type": "object", "properties": {}}
    obj_hints = typing.get_type_hints(obj, localns={"Scaffold": Scaffold})
    obj_attrs = get_config_attributes(obj)
    for attr, descr in obj_attrs.items():
        hint = obj_hints.get(attr, str)
        schema["properties"][attr] = attr_schema(hint)

    return schema

def attr_schema(hint):
    schema = {}
    if hint is str:
        schema["type"] = "string"
    elif hint is int:
        schema["type"] = "integer"
    elif hint is float:
        schema["type"] = "number"
    elif hint is bool:
        schema["type"] = "boolean"
    elif typing.get_origin(hint) is list:
        schema["type"] = "array"
        schema["items"] = attr_schema(typing.get_args(hint)[0])
    elif typing.get_origin(hint) is dict:
        schema["type"] = "object"
        schema["properties"] = {}
        schema["additionalProperties"] = attr_schema(typing.get_args(hint)[1])
    else:
        try:
            is_node = get_config_attributes(hint)
        except:
            is_node = False
        if is_node:
            schema = object_schema(hint)
        else:
            schema["type"] = "object"
            schema["properties"] = {}
            schema["description"] = f"Could not determine schema of type {hint}"

    return schema

from bsb.config import Configuration

print(schema(Configuration))
