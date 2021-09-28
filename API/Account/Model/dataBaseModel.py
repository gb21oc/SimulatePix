import hashlib
from random import randint
from datetime import datetime
from Util.config import msgExcept, SALT_KEY
from DataBase.connection import dbAccount


class dataBaseModel:
    def __init__(self, idAccount=None, fullName=None, cpf=None, email=None, account=None, password=None,
                 balance=None, randomKey=None):
        self.cpf = cpf
        self.email = email
        self.balance = balance
        self.account = account
        self.fullName = fullName
        self.idAccount = idAccount
        self.randomKey = randomKey
        self.password = password

    def find(self):
        try:
            findCpf = [i for i in dbAccount.find({"cpf": self.cpf})]
            findEmail = [i for i in dbAccount.find({"email": self.email})]
            findAccount = [i for i in dbAccount.find({"account": self.account})]
            findRandomKey = [i for i in dbAccount.find({"randomKey": self.randomKey})]
            if len(findCpf) <= 1 and len(findEmail) <= 1 and len(findAccount) <= 1 and len(findRandomKey) <= 1:
                return ""
            return {"message": "It is not possible to register the account as there is already another one with the same information"}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

    def insert(self):
        try:
            dateNow = datetime.now().strftime("%d/%m/%Y")
            self.password = self.password + SALT_KEY
            self.randomKey = self.fullName + self.cpf + self.email + SALT_KEY
            self.balance = 500
            self.account = ""
            for i in range(6):
                digit = randint(0, 10)
                if i == 5:
                    self.account += f"-{digit}"
                else:
                    self.account += f"{digit}"
            dbAccount.insert_one({
                "name": self.fullName,
                "cpf": self.cpf,
                "email": self.email,
                "password": hashlib.md5(self.password.encode("UTF-8")).hexdigest(),
                "account": self.account,
                "randomKey": hashlib.md5(self.randomKey.encode("UTF-8")).hexdigest(),  # Faze com hash do nome, cpf e email + SALT_KEY
                "balance": self.balance,
                "dateCreate": dateNow,
                "dateUpdate": None
            })
            return {"message": f"Account created successfully, welcome {self.fullName}"}, 201
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

