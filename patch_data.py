from flask import abort, request, jsonify
from jsonschema import validate

from citizen_mdl import Citizen, unpack_relatives_to_int_list, pack_relatives_to_db_format
from data_validation import validate_date, validate_id_not_in_relatives
from database import db

# Схема валидации для PATCH запроса
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


# Удаляет citizen_id из списка родственников пользователя с id = relative_id
def remove_cur_citizen_from_other_relative(relative_id, citizen_id, import_id):
    citizen = Citizen.query.filter_by(citizen_id=relative_id, dataset_id=import_id).first()
    print(citizen)
    if citizen is None:
        raise ValueError
    else:
        try:
            relatives_list = unpack_relatives_to_int_list(citizen.relatives)
            relatives_list.remove(citizen_id)
            relatives_list.sort()
            packed_relatives = pack_relatives_to_db_format(relatives_list)
            citizen.relatives = packed_relatives
        except ValueError as e:
            raise e


# Добавляет в список родственников пользователя
# с id = relative_id пользователя citizen_id
def add_cur_citizen_to_other_relative(relative_id, citizen_id, import_id):
    citizen = Citizen.query.filter_by(citizen_id=relative_id, dataset_id=import_id).first()
    if citizen is None:
        raise ValueError("Citizens is none here!")
    else:
        relatives_list = unpack_relatives_to_int_list(citizen.relatives)
        relatives_list.append(citizen_id)
        relatives_list.sort()
        packed_relatives = pack_relatives_to_db_format(relatives_list)
        citizen.relatives = packed_relatives


def main(import_id, citizen_id):
    # Пытаемся парсить пришедие данные, как JSON.
    if request.get_json(silent=True) is None:
        # Если не удалось распарсить, выбрасываем исключение.
        raise ValueError("request data can't be parsed as json")
    # Получаем соответствующего жителя по двум
    # основным ключам -- номеру выгрузки и id.
    citizen = Citizen.query.filter_by(citizen_id=citizen_id, dataset_id=import_id).first()
    if citizen is None:
        # Если не нашли такого пользователя, выбрасываем исключение.
        raise ValueError("Citizen with such citizen_id and import_id wasn't found")
    else:
        citizen_obj = request.json
        # Общая валидация PATCH-схемы.
        validate(instance=citizen_obj, schema=dataset_patch_schema)
        # Валидация отдельных полей. Проще сделать её вручную.
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
            # Получим два сета с id пользователей
            prev_relatives_list = unpack_relatives_to_int_list(citizen.relatives)
            cur_relatives_list = citizen_obj['relatives']
            prev_relatives = set(prev_relatives_list)
            cur_relatives = set(cur_relatives_list)
            # todo: Нужно ли посортить?
            # Получим разницу в обоих случаях и
            # удалим/добавим необходимые id
            for relative_id in prev_relatives.difference(cur_relatives):
                remove_cur_citizen_from_other_relative(relative_id, citizen_id, import_id)
            for relative_id in cur_relatives.difference(prev_relatives):
                add_cur_citizen_to_other_relative(relative_id, citizen_id, import_id)
            citizen.relatives = pack_relatives_to_db_format(citizen_obj['relatives'])
        # Добавим в базу данных.
        db.session.commit()
        res = {
            "data": citizen.json_representation()
        }
        return jsonify(res), 200


