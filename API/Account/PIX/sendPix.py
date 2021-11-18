from utilConfig import msgExcept
from Util.validators import Validate
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from MyException.ApiException import ValidateError
from Account.Model.dataBaseModel import dataBaseModel


class SendPix(Resource):
    args = reqparse.RequestParser()
    args.add_argument("cpf", type=str, help="The 'cpf' field is required", required=True)
    args.add_argument("randomKey", type=str, required=True)
    args.add_argument("account_sender", type=str, help="The 'account' field is required", required=True)
    args.add_argument("account_dst", type=str, help="The 'account' field is required", required=True)
    args.add_argument("pix", type=int, help="The 'pix' field is required", required=True)

    @jwt_required()
    def post(self):
        data = self.args.parse_args()
        try:
            Validate(cpf=data["cpf"], account=data["account_sender"], randomKey=data["randomKey"]).valida()
            if data["account_dst"] is not None:
                returnPix = dataBaseModel(cpf=data["cpf"], account=data["account_sender"], randomKey=data["randomKey"])\
                    .sendPix(account=data["account_dst"], pix=data["pix"])
                return returnPix
            return {"message": "Account destiny not found"}, 400
        except ValidateError as err:
            return {'message': str(err)}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500




