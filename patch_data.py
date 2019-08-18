from flask import abort, request
from jsonschema import validate, exceptions

from citizen_mdl import Citizen
from data_validation import validate_date, validate_id_not_in_relatives, do_single_citizen_validations
from dataset_mdl import Dataset

dataset_patch_schema = {
    "type": "object",
    "properties": {
        "town": {
            "type": "string",
            "minLength": 1
        },
        "street": {
            "type": "string",
            "minLength": 1
        },
        "building": {
            "type": "string",
            "minLength": 1
        },
        "apartment": {
            "type": "number",
            "minimum": 0
        },
        "name": {
            "type": "string",
            "minLength": 1
        },
        "birth_date": {
            "type": "string",
            "pattern": "^\d{2}\.\d{2}\.\d{4}$"
        },
        "gender": {
            "type": "string",
            "pattern": "^(male|female)$"
        },
        "relatives": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "uniqueItems": True
        }
    },
    "anyOf": [
        {"required": ["town"]},
        {"required": ["street"]},
        {"required": ["building"]},
        {"required": ["apartment"]},
        {"required": ["name"]},
        {"required": ["birth_date"]},
        {"required": ["gender"]},
        {"required": ["relatives"]}
    ],
    "additionalProperties": False,

}


def main(import_id, citizen_id):
    if not request.json:
        abort(400)
    citizen = Citizen.query.filter_by(id=citizen_id, dataset_id=import_id).first()
    try:
        if citizen is None:
            raise ValueError
        else:
            try:
                citizen_obj = request.json
                validate(instance=citizen_obj, schema=dataset_patch_schema)
                do_single_citizen_validations(citizen_obj)

            except (exceptions.ValidationError, ValueError):
                abort(400)
    except ValueError:
        abort(400)


