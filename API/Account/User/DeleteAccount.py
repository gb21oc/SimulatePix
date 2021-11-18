from utilConfig import msgExcept
from Util.validators import Validate
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from MyException.ApiException import ValidateError
from Account.Model.dataBaseModel import dataBaseModel


class DeleteAccount(Resource):
    args = reqparse.RequestParser()
    args.add_argument("cpf", type=str, help="The 'cpf' field is required", required=True)
    args.add_argument("account", type=str, required=True)
    args.add_argument("randomKey", type=str, required=True)

    @jwt_required()
    def delete(self):
        data = self.args.parse_args()
        try:
            Validate(**data).valida()
            delUser = dataBaseModel(**data).deleteUser()
            return delUser
        except ValidateError as err:
            return {'message': str(err)}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500
