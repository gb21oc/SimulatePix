from Util.sendEmail import SendEmail
from Util.validators import Validate
from utilConfig import msgExcept, ip
from flask_restful import Resource, reqparse
from MyException.ApiException import ValidateError
from Account.Model.dataBaseModel import dataBaseModel


class Login(Resource):
    args = reqparse.RequestParser()
    args.add_argument("cpf", type=str, help="The 'cpf' field is required", required=True)
    args.add_argument("password", type=str, help="The 'password' field is required", required=True)

    def post(self):
        data = self.args.parse_args()
        try:
            Validate(**data).valida()
            model = dataBaseModel(**data).findOneLogin()
            SendEmail(fullName=model[0]["data"]["name"], email=model[0]["data"]["email"], ip=ip).send(
                "Login", "Hello we are here just to let you know that we have received a login request")
            return model
        except ValidateError as err:
            return {'message': str(err)}, 400
        except Exception as err:
            print(str(err))
            return {'message': msgExcept}, 500

