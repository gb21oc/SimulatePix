from utilConfig import msgExcept
from Util.validators import Validate
from Util.sendEmail import SendEmail
from flask_restful import Resource, reqparse
from MyException.ApiException import ValidateError
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
            Validate(**data).valida()
            model = dataBaseModel(**data)
            verifyAccount = model.find()
            if verifyAccount == "":
                user = model.insert()
                account = model.findAccount()
                SendEmail(data["email"], data["password"], data["fullName"], account
                          ).send("Create", "Account Creation")
                return user
            return verifyAccount
        except ValidateError as err:
            return {'message': str(err)}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500
