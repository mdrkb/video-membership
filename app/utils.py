import json
from pydantic import BaseModel, error_wrappers


def valid_schema_or_error(raw_data: dict, schema: BaseModel):
    data = {}
    errors = []
    error_str = None
    try:
        cleaned_data = schema(**raw_data)
        data = cleaned_data.dict()
    except error_wrappers.ValidationError as e:
        error_str = e.json()

    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc": "non_field_error", "msg": "Unknown error"}]

    return data, errors
