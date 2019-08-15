from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\MyWorkRep\\backend-school-task\\database.dt'
db = SQLAlchemy(app)

citizen_id = 0


def inc_citizen_id():
    global citizen_id
    citizen_id += 1
    return citizen_id


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'Dataset %r' % self.id


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), primary_key=True)
    dataset = db.relationship('Dataset', backref=db.backref('citizens'))

    def __repr__(self):
        return 'Citizen %r cit_id %r' % (self.dataset, self.id)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

