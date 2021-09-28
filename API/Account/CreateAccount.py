from Util.config import msgExcept
from flask_restful import Resource, reqparse
from Account.Model.dataBaseModel import dataBaseModel


class CreateAccount(Resource):
    args = reqparse.RequestParser()
    args.add_argument("cpf", type=str, help="The 'cpf' field is required", required=True)
    args.add_argument("email", type=str, help="The 'email' field is required", required=True)
    args.add_argument("password", type=str, help="The 'password' field is required", required=True)
    args.add_argument("fullName", type=str, help="The 'full name' field is required", required=True)

    def post(self):
        data = self.args.parse_args()
        try:
            model = dataBaseModel(**data)
            verifyAccount = model.find()
            if verifyAccount == "":
                return model.insert()
            return verifyAccount
        except (Exception, ValueError, IndexError) as err:
            print(err)
            return {'message': msgExcept}, 500
