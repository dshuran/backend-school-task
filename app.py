import os.path

from flask import Flask

import get_data
import import_data
import patch_data
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\MyWorkRep\\backend-school-task\\database.dt'
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/imports', methods=['POST'])
def do_import_data():
    # todo обёртку try/except для разных исключений.
    return import_data.main()


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def do_get_data(import_id):
    # todo обёртку try/except для разных исключений.
    return get_data.main(int(import_id))


@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def do_patch_data(import_id, citizen_id):
    # todo обёртку try/except для разных исключений.
    return patch_data.main(int(import_id), int(citizen_id))


def setup_database():
    with app.app_context():
        db.create_all()


def main():
    if not os.path.isfile('D:\\MyWorkRep\\backend-school-task\\database.dt'):
        setup_database()
    app.run(debug=True)


if __name__ == '__main__':
    main()



