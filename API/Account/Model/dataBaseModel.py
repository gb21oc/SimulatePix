import hashlib
import json

from bson import json_util
from flask import jsonify
from random import randint
from datetime import datetime
from DataBase.connection import dbAccount
from Util.config import msgExcept, SALT_KEY
from flask_jwt_extended import create_access_token, get_jwt


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
            if len(findCpf) < 1 and len(findEmail) < 1 and len(findAccount) < 1 and len(findRandomKey) < 1:
                return ""
            return {"message": "It is not possible to register the account as there is already another one with the same information"}, 400
        except (Exception, ValueError, IndexError) as err:
            print(str(err))
            return {'message': msgExcept}, 500

    def findOne(self):
        try:
            passwd = self.password + SALT_KEY
            self.password = hashlib.md5(passwd.encode("UTF-8")).hexdigest()
            user = dbAccount.find_one({
                "cpf": self.cpf,
                "password": hashlib.sha256(self.password.encode("UTF-8")).hexdigest()
            }, {"_id", "name", "cpf", "email", "account", "randomKey", "balance"})
            if user is None:
                return {"message": "Incorrect email or password"}, 400
            token = create_access_token(identity=f"{user['_id']}")
            concInfo = f"{user['name']}${user['cpf']}${user['email']}${SALT_KEY}"
            updateToken = hashlib.sha256(concInfo.encode("UTF-8")).hexdigest()
            return {"token": f"{token}", "secureTokenUpdate": updateToken, "data": json.loads(json_util.dumps(user))}, 200
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

    def findAccount(self):
        try:
            findCpf = [i for i in dbAccount.find({"cpf": self.cpf})]
            if len(findCpf) == 1:
                return findCpf[0]["account"]
            return {"message": "Could not find account"}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

    def insert(self):
        try:
            dateNow = datetime.now().strftime("%d/%m/%Y")
            passwd = self.password + SALT_KEY
            self.password = hashlib.md5(passwd.encode("UTF-8")).hexdigest()
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
                "password": hashlib.sha256(self.password.encode("UTF-8")).hexdigest(),
                "account": self.account,
                "randomKey": hashlib.md5(self.randomKey.encode("UTF-8")).hexdigest(),  # Faze com hash do nome, cpf e email + SALT_KEY self.randomKey.encode("UTF-8")
                "balance": self.balance,
                "dateCreate": dateNow,
                "dateUpdate": None
            })
            return {"message": f"Account created successfully, welcome {self.fullName}"}, 201
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

