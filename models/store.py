import sqlite3

from db import db

class StoreModel(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    street = db.Column(db.String())
    city = db.Column(db.String())
    province = db.Column(db.String())

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, street, city, province):
        self.name = name
        self.street = street
        self.city = city
        self.province = province

    @classmethod
    def get_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def list_items(cls):
        result = cls.query.all()
        return result

    def convert_to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "street":self.street,
            "city":self.city,
            "province":self.province,
            "items":[f.convert_to_dict() for f in self.items.all() if self.items is not None],
        }
