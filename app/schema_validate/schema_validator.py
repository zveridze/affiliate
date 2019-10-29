from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
import os
from validate_email import validate_email


def convert_to_dict(schema):
    file_json = os.path.join(os.path.dirname(__file__), schema)
    with open(file_json) as f:
        dict_data = json.load(f)
    return dict_data


def validate_data(data, schema):
    schema_data = convert_to_dict(schema)
    try:
        validate(data, schema_data)
    except ValidationError as exception:
        return exception.message

    if validate_email(data['email']) is False:
        return 'Email invalid'
