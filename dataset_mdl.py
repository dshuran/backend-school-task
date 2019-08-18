from database import db


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'Dataset %r: %r' % (self.id, self.citizens)