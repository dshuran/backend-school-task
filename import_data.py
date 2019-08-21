from flask import request, abort, jsonify
from dataset_mdl import Dataset
from citizen_mdl import Citizen, id_separator
from dataset_counter_mdl import get_dataset_counter
from jsonschema import validate, exceptions
from database import db

from data_validation import validate_relatives, validate_citizens_ids_intersection, \
     do_single_citizen_validations


main_schema = {
    "type": "object",
    "properties": {
        "citizens": {
            "type": "array",
            "items": {"$ref": "#/definitions/inner_schema"},
            "minItems": 1
        }
    },
    "required": ["citizens"],
    "additionalProperties": False,
    "definitions": {
        "inner_schema": {
            "type": "object",
            "properties": {
                "citizen_id": {
                    "type": "number",
                    "minimum": 0
                },
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
            "required": ["citizen_id", "town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"],
            "additionalProperties": False
        }
    }
}


def main():
    try:
        if request.get_json(silent=True) is None:  # more checks
            print('there! In parsing JSON')
            abort(400)
        validate(instance=request.json, schema=main_schema)
    except (exceptions.ValidationError, ValueError) as e:
        print(e)
        abort(400)
    citizens = request.json['citizens']
    dataset_counter = get_dataset_counter()
    # Если будет неудача, то import_id не изменится
    dataset = Dataset(id=(dataset_counter.counter + 1))
    # todo: больше проверок на формат данных здесь. Что вообще есть поле citizens, что оно итерабельное. -- Учитывается в type: object схемы.
    # todo: Для этого нужно просто чек, что request.json['citizens'] type object в другой схеме
    for citizen_obj in citizens:
        try:
            # validate(instance=citizen_obj, schema=dataset_import_inner_schema)
            # Мы знаем, что как минимум, relatives - список интов.
            do_single_citizen_validations(citizen_obj)
            # handle in except any other error
        except (exceptions.ValidationError, ValueError) as e:
            print(e)
            abort(400)
        citizen = Citizen(
            citizen_id=citizen_obj['citizen_id'],  # check, что нет такого же айди в выгрузке
            town=citizen_obj['town'],
            street=citizen_obj['street'],
            building=citizen_obj['building'],
            apartment=citizen_obj['apartment'],
            name=citizen_obj['name'],
            birth_date=citizen_obj['birth_date'],
            gender=citizen_obj['gender'],
            relatives=id_separator.join(map(str, citizen_obj['relatives'])), # todo: заменить на pack relatives to string
            dataset=dataset)
    try:
        validate_citizens_ids_intersection(dataset.citizens)
        validate_relatives(dataset.citizens)
    except (ValueError, KeyError) as e:
        print(e)
        abort(400)
    # Данные корректны, добавим в бд.
    db.session.add(dataset)
    db.session.commit()
    success_response = {
        "data": {
            "import_id": dataset_counter.inc()
        }
    }
    return jsonify(success_response), 201
