from database import db

singleton_dataset_id = 1


class DatasetCounter(db.Model):
    # SINGLETON
    id = db.Column(db.Integer, primary_key=True)  # Всегда должен быть = 1
    counter = db.Column(db.Integer, nullable=False)

    def inc(self):
        self.counter += 1
        db.session.commit()
        return self.counter

    def __repr__(self):
        return 'Import Counter id = %r counter = %r' % (self.id, self.counter)


def get_dataset_counter():
    dataset_counter = DatasetCounter.query.filter_by(id=singleton_dataset_id).first()
    if dataset_counter is None:
        dataset_counter = DatasetCounter(id=singleton_dataset_id, counter=0)
        db.session.add(dataset_counter)
        db.session.commit()
    return dataset_counter
