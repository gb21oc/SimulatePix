from Account.PIX.sendPix import SendPix
from Account.User.LoginAccount import Login
from Account.User.DeleteAccount import DeleteAccount
from Account.User.UpdateAccount import UpdateAccount
from Account.User.CreateAccount import CreateAccount


class Endpoints:
    def __init__(self, api):
        self.api = api

    def returnEndpoint(self):
        # User
        self.api.add_resource(CreateAccount, "/createAccount")
        self.api.add_resource(Login, "/login")
        self.api.add_resource(UpdateAccount, "/update")
        self.api.add_resource(DeleteAccount, "/del")
        # Pix
        self.api.add_resource(SendPix, "/pix")
