from flask import abort, request, jsonify
from jsonschema import validate

from citizen_mdl import Citizen, unpack_relatives_to_int_list, pack_relatives_to_db_format
from data_validation import validate_date, validate_id_not_in_relatives
from database import db

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


def remove_cur_citizen_from_other_relative(relative_id, citizen_id, import_id):
    print('relat id = ', relative_id, ' cit id = ', citizen_id, 'import id = ', import_id)
    citizen = Citizen.query.filter_by(citizen_id=relative_id, dataset_id=import_id).first()
    print(citizen)
    if citizen is None:
        raise ValueError
    else:
        try:
            relatives_list = unpack_relatives_to_int_list(citizen.relatives)
            print(relatives_list, ' id = ', citizen_id)
            print(type(citizen_id))
            relatives_list.remove(citizen_id)
            print('there')
            packed_relatives = pack_relatives_to_db_format(relatives_list)
            citizen.relatives = packed_relatives
        except ValueError as e:
            raise e


def add_cur_citizen_to_other_relative(relative_id, citizen_id, import_id):
    citizen = Citizen.query.filter_by(citizen_id=relative_id, dataset_id=import_id).first()
    if citizen is None:
        raise ValueError("Citizens is none here!")
    else:
        relatives_list = unpack_relatives_to_int_list(citizen.relatives)
        relatives_list.append(citizen_id)
        packed_relatives = pack_relatives_to_db_format(relatives_list)
        citizen.relatives = packed_relatives


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
            # todo: Нужно ли посортить?
            try:
                for relative_id in prev_relatives.difference(cur_relatives):
                    remove_cur_citizen_from_other_relative(relative_id, citizen_id, import_id)
                for relative_id in cur_relatives.difference(prev_relatives):
                    add_cur_citizen_to_other_relative(relative_id, citizen_id, import_id)
            except ValueError as e:
                print(e)
                abort(400)
            citizen.relatives = pack_relatives_to_db_format(citizen_obj['relatives'])
        db.session.commit()
        res = {
            "data": citizen.json_representation()
        }
        return jsonify(res), 200


