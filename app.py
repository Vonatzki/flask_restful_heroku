import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'vonatzki'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/api/item/<string:name>')
api.add_resource(ItemList, '/api/items')
api.add_resource(UserRegister, '/api/users/register')
api.add_resource(UserList, '/api/users')
api.add_resource(Store, '/api/store/<string:name>')
api.add_resource(StoreList, '/api/stores')

if __name__ == '__main__':

    from db import db

    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    app.run(port=5000, debug=True)
