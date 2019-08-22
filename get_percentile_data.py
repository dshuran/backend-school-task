from flask import jsonify

from dataset_mdl import Dataset
from datetime import date
import numpy as np


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_citizen_age(birth_date):
    day, month, year = map(int, birth_date.split('.'))
    assert isinstance(month, int)
    date_obj = date(year, month, day)
    return calculate_age(date_obj)


def main(import_id):
    dataset = Dataset.query.filter_by(id=import_id).first()
    citizens = dataset.citizens
    ages_in_town = {}
    for citizen in citizens:
        if citizen.town not in ages_in_town:
            ages_in_town[citizen.town] = []
        citizen_age = get_citizen_age(citizen.birth_date)
        assert isinstance(citizen_age, int)
        ages_in_town[citizen.town].append(citizen_age)
    res = []
    for town in ages_in_town:
        print('HERE')
        print(ages_in_town[town])
        p50 = np.percentile(ages_in_town[town], 50)
        p75 = np.percentile(ages_in_town[town], 75)
        p99 = np.percentile(ages_in_town[town], 99)
        res.append({
            "town": town,
            "p50": float("{0:.2f}".format(p50)),
            "p75": float("{0:.2f}".format(p75)),
            "p99": float("{0:.2f}".format(p99))
        })
    final_output = {
        "data": res
    }
    return jsonify(final_output), 200




