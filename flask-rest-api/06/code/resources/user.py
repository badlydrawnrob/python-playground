'''
Add in the UserModel
'''

from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}

        # You can remove `data['username'], data['password']`
        # and unpack data instead: http://bit.ly/2rzVCdz
        # - this is safe to do as we're using `parser`
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully'}, 201