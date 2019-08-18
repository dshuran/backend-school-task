from flask import Flask
from database import db
import get_data, import_data
import os.path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\MyWorkRep\\backend-school-task\\database.dt'
app.config['JSON_SORT_KEYS'] = False
db.init_app(app)


@app.route('/imports', methods=['POST'])
def do_import_data():
    # todo обёртку try/except для разных исключений.
    return import_data.main()


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def do_get_data(import_id):
    # todo обёртку try/except для разных исключений.
    return get_data.main(import_id)


def setup_database():
    with app.app_context():
        db.create_all()


def main():
    if not os.path.isfile('D:\\MyWorkRep\\backend-school-task\\database.dt'):
        setup_database()
    app.run(debug=True)


if __name__ == '__main__':
    main()



