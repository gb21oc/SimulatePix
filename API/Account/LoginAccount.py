from utilConfig import msgExcept, ip
from datetime import datetime
from Util.sendEmail import SendEmail
from Util.validators import Validate
from flask_restful import Resource, reqparse
from Account.Model.dataBaseModel import dataBaseModel


class Login(Resource):
    args = reqparse.RequestParser()
    args.add_argument("cpf", type=str, help="The 'cpf' field is required", required=True)
    args.add_argument("password", type=str, help="The 'password' field is required", required=True)

    def post(self):
        data = self.args.parse_args()
        try:
            validate = Validate(**data).valida()
            if validate == "":
                model = dataBaseModel(**data).findOne()
                SendEmail(fullName=model[0]["data"]["name"], email=model[0]["data"]["email"], ip=ip).send("Login", "Hello we are here just to let you know that we have received a login request")
                return model
            return {"message": validate}, 400
        except (Exception, ValueError, IndexError) as err:
            print(err)
            return {'message': msgExcept}, 500

