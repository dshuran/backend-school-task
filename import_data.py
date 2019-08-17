from flask import request, abort, jsonify
from app import Citizen, get_dataset_counter
from jsonschema import validate, draft7_format_checker, FormatChecker, exceptions
import datetime

dataset_import_schema = {
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
    "additionalProperties": False,
}


def do_external_checks(citizen_obj):
    validate_date(citizen_obj['birth_date'])


def validate_date(date_string):
    day, month, year = map(int, date_string.split('.'))
    date = datetime.date(year, month, day)


def main():
    if not request.json:  # more checks
        abort(400)
    citizens = request.json['citizens']
    for citizen_obj in citizens:
        try:
            validate(instance=citizen_obj, schema=dataset_import_schema)
            do_external_checks(citizen_obj)
        except (exceptions.ValidationError, ValueError):
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
            relatives=citizen_obj['relatives']) # check, что нет самого себя в родственниках
        # add to db
    dataset_counter = get_dataset_counter()
    success_response = {
        "data": {
            "import_id": dataset_counter.inc()
        }
    }
    return jsonify(success_response), 201
