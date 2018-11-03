from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from config.meta import DATABASE_PATH
from config.db_orm import connect_to_database
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!",
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id!",
    )

    @jwt_required()
    def get(self, name):

        item = ItemModel.get_item_by_name(name)

        if item:
            return {"item":item.convert_to_dict()}, 200
        else:
            return {"item":None}, 404

    @jwt_required()
    def post(self, name):

        if ItemModel.get_item_by_name(name) is not None:
            return {'message':f'An item with "{name}" already exists.'}, 409

        data = Item.parser.parse_args()
        data['name'] = name

        item = ItemModel(**data)
        item.save_to_db()

        item = ItemModel.get_item_by_name(name)

        if item:
            return item.convert_to_dict(), 201
        else:
            return {'message':"Add item action failed!"}, 500

    @jwt_required()
    def delete(self, name):

        item = ItemModel.get_item_by_name(name)

        if item:
            item.delete_from_db()
            return {'message':'Item deleted'}, 201
        else:
            return {'message':'Item to delete not found!'}, 404


    @jwt_required()
    def put(self, name):

        item = ItemModel.get_item_by_name(name)
        data = Item.parser.parse_args()

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.convert_to_dict()


class ItemList(Resource):

    def get(self):
        return {
            "items":[f.convert_to_dict() for f in ItemModel.query.all()],
        }
