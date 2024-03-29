import os

from flask import Flask, abort

from Controller import get_percentile_data, patch_data, import_data, get_presents_data, get_data
from database import db

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/imports', methods=['POST'])
def do_import_data():
    try:
        return import_data.main()
    except Exception as e:
        handle_exception(e)


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def do_get_data(import_id):
    try:
        return get_data.main(int(import_id))
    except Exception as e:
        handle_exception(e)


@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def do_patch_data(import_id, citizen_id):
    try:
        return patch_data.main(int(import_id), int(citizen_id))
    except Exception as e:
        handle_exception(e)


@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def do_get_presents_data(import_id):
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
    abort(400)


def main():
    if not os.path.isfile(db_path):
        setup_database()
    app.run(host='0.0.0.0', port='8080')


if __name__ == '__main__':
    main()
