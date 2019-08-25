import os.path

from flask import Flask, abort

from Controller import get_percentile_data, patch_data, import_data, get_presents_data, get_data
import traceback
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:benben12@localhost:5432/tmp'
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/imports', methods=['POST'])
def do_import_data():
    # todo обёртку try/except для разных исключений.
    try:
        return import_data.main()
    except Exception as e:
        handle_exception(e)


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def do_get_data(import_id):
    # todo обёртку try/except для разных исключений.
    try:
        return get_data.main(int(import_id))
    except Exception as e:
        handle_exception(e)


@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def do_patch_data(import_id, citizen_id):
    # todo обёртку try/except для разных исключений.
    try:
        return patch_data.main(int(import_id), int(citizen_id))
    except Exception as e:
        handle_exception(e)


@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def do_get_presents_data(import_id):
    # todo обёртку try/except для разных исключений.
    try:
        return get_presents_data.main(int(import_id))
    except Exception as e:
        handle_exception(e)


@app.route('/imports/<import_id>/towns/stat/percentile/age', methods=['GET'])
def do_get_percentile_data(import_id):
    try:
        return get_percentile_data.main(int(import_id))
    except Exception as e:
        handle_exception(e)


def setup_database():
    with app.app_context():
        db.create_all()


def handle_exception(e):
    print(e)
    print(traceback.format_exc())
    abort(400)


def main():
    setup_database()
    app.run(debug=True)


if __name__ == '__main__':
    main()



