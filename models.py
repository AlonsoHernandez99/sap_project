from app import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'Name: {self.name}, '
            f'LastName: {self.lastname}, '
            f'Email: {self.email}'
        )
