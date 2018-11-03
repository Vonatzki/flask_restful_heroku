from config.meta import DATABASE_PATH
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean())

    def __init__(self, username, password, admin):
        self.username=username
        self.password=password
        self.admin=admin

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user

    @classmethod
    def find_by_id(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def convert_to_dict(self):

        return dict(
            username=self.username,
            admin=self.admin,
        )
