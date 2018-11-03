from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'street',
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        'city',
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        'province',
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )

    def get(self, name):
        store = StoreModel.get_item_by_name(name)
        if store:
            return store.convert_to_dict(), 200

        return {'message':'Store not found'}, 404

    @jwt_required()
    def post(self, name):

        data = Store.parser.parse_args()

        if StoreModel.get_item_by_name(name):
            return {'message':f'A store with "{name}" already exists.'}, 400

        data['name'] = name

        store = StoreModel(**data)

        try:
            store.save_to_db()
        except:
            return {'message':"An error occurred while creating the store."}, 500

        return store.convert_to_dict(), 201

    @jwt_required()
    def put(self, name):

        data = Store.parser.parse_args()

        store = StoreModel.get_item_by_name(name)

        if store:
            store.street = data['street']
            store.city = data['city']
            store.province = data['province']

        else:
            data['name'] = name
            store = StoreModel(**data)

        store.save_to_db()

        return store.convert_to_dict(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.get_item_by_name(name)

        if store:
            store.delete_from_db()
            return {"message":"Store deleted!"}, 201

        else:
            return {"message":"Store to delete not found!"}, 404


class StoreList(Resource):
    def get(self):
        return {
            "stores":[f.convert_to_dict() for f in StoreModel.query.all()]
        }
