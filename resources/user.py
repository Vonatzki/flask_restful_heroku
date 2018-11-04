from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import UserModel

from config.meta import DATABASE_PATH

class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank!",
    )

    parser.add_argument(
        'admin',
        type=bool,
        required=True,
        help="This field cannot be left blank!",
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'A user with that username already exists!'}, 409

        user = UserModel(**data)
        user.save_to_db()

        return {'message':'User has successfully registered!'}, 201


class UserList(Resource):

    def get(self):

        return {'users':[f.convert_to_dict() for f in UserModel.query.all()]}
