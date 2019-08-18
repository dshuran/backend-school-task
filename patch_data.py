from flask import abort, request, jsonify
from jsonschema import validate, exceptions

from citizen_mdl import Citizen, pack_relatives_to_string, unpack_relatives_to_int_list, pack_relatives_to_db_format
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


def remove_cur_citizen_from_other_relatives(relative, citizen_id):
    pass


def add_cur_citizen_to_other_relatives(relative_id, citizen_id):
    pass


def main(import_id, citizen_id):
    if not request.json:
        abort(400)
    citizen = Citizen.query.filter_by(citizen_id=citizen_id, dataset_id=import_id).first()
    if citizen is None:
        raise ValueError
    else:
        citizen_obj = request.json
        validate(instance=citizen_obj, schema=dataset_patch_schema)
        if 'birth_date' in citizen_obj:
            validate_date(citizen_obj['birth_date'])
        if 'relatives' in citizen_obj:
            validate_id_not_in_relatives(citizen.citizen_id, citizen_obj['relatives'])
        # Валидация закончена
        print('HERE')
        print(type(citizen_obj))
        if 'town' in citizen_obj:
            citizen.town = citizen_obj['town']
        if 'street' in citizen_obj:
            citizen.street = citizen_obj['street']
        if 'building' in citizen_obj:
            citizen.building = citizen_obj['building']
        if 'apartment' in citizen_obj:
            citizen.apartment = citizen_obj['apartment']
        if 'name' in citizen_obj:
            citizen.name = citizen_obj['name']
        if 'birth_date' in citizen_obj:
            citizen.birth_date = citizen_obj['birth_date']
        if 'gender' in citizen_obj:
            citizen.gender = citizen_obj['gender']
        if 'relatives' in citizen_obj:
            prev_relatives_list = unpack_relatives_to_int_list(citizen.relatives)
            cur_relatives_list = citizen_obj['relatives']
            prev_relatives = set(prev_relatives_list)
            cur_relatives = set(cur_relatives_list)
            for relative_id in prev_relatives.difference(cur_relatives):
                remove_cur_citizen_from_other_relatives(relative_id, citizen_id)
            for relative_id in cur_relatives.difference(prev_relatives):
                add_cur_citizen_to_other_relatives(relative_id, citizen_id)
            # todo: привести бд в консистентное состояние
            citizen.relatives = pack_relatives_to_db_format(citizen_obj['relatives'])
        res = {
            "data": citizen.json_representation()
        }
        return jsonify(res), 200


