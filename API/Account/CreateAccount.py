from Util.config import msgExcept
from Util.sendEmail import SendEmail
from Util.validators import Validate
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
            validate = Validate(**data).valida()
            if validate == "":
                model = dataBaseModel(**data)
                verifyAccount = model.find()
                if verifyAccount == "":
                    user = model.insert()
                    account = model.findAccount()
                    SendEmail(data["email"], data["password"], data["fullName"], account
                              ).send("Account Creation")
                    return user
                return verifyAccount
            return {"message": validate}, 400
        except (Exception, ValueError, IndexError) as err:
            print(err)
            return {'message': msgExcept}, 500
