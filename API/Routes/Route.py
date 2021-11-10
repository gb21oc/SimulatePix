from Account.CreateAccount import CreateAccount
from Account.LoginAccount import Login


class Endpoints:
    def __init__(self, api):
        self.api = api

    def returnEndpoint(self):
        self.api.add_resource(CreateAccount, "/createAccount")
        self.api.add_resource(Login, "/login")
