from Account.CreateAccount import CreateAccount


class Endpoints:
    def __init__(self, api):
        self.api = api

    def returnEndpoint(self):
        self.api.add_resource(CreateAccount, "/createAccount")
