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
    citizen = Citizen.query.filter_by(citizen_id=citizen_id, dataset_id=import_id).first()
    try:
        if citizen is None:
            raise ValueError
        else:
            try:
                citizen_obj = request.json
                validate(instance=citizen_obj, schema=dataset_patch_schema)
                if 'birth_date' in citizen_obj:
                    validate_date(citizen_obj['birth_date'])
                if 'relatives' in citizen_obj:
                    validate_id_not_in_relatives(citizen.citizen_id, citizen_obj['relatives'])
                if 'town' in citizen_obj:
                    citizen_obj.town = citizen_obj['town']
                if 'street' in citizen_obj:
                    citizen_obj.street = citizen_obj['street']
                if 'building' in citizen_obj:
                    citizen_obj.building = citizen_obj['building']
                if 'apartment' in citizen_obj:
                    citizen_obj.apartment = citizen_obj['apartment']
                if 'name' in citizen_obj:
                    citizen_obj.name = citizen_obj['name']
                if 'birth_date' in citizen_obj:
                    citizen_obj.birth_date = citizen_obj['birth_date']
                if 'gender' in citizen_obj:
                    citizen_obj.gender = citizen_obj['gender']
                if 'relatives' in citizen_obj:
                    prev_relatives = citizen_obj.relatives
                    cur_relatives = citizen_obj['relatives']
                    # todo: привести бд в консистентное состояние
                    citizen_obj.relatives = citizen_obj['relatives']
            except (exceptions.ValidationError, ValueError):
                abort(400)
    except ValueError:
        abort(400)


