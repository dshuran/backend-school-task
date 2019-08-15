from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import upload_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\MyWorkRep\\backend-school-task\\database.dt'
db = SQLAlchemy(app)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'Dataset %r' % self.id


class Citizen(db.Model):
    citizen_id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    apartment = db.Column(db.Integer)
    name = db.Column(db.String)
    birth_date = db.Column(db.DATETIME)
    gender = db.Column(db.String)
    relatives = db.Column(db.ARRAY(db.Integer))

    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), primary_key=True)
    dataset = db.relationship('Dataset', backref=db.backref('citizens'))

    def __repr__(self):
        return 'Citizen %r cit_id %r' % (self.dataset, self.id)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/imports', methods=['POST'])
def upload_data():
    upload_data.main()


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

