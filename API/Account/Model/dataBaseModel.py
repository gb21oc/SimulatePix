import json
import hashlib
# from flask import request
from bson import json_util
from random import randint
from datetime import datetime
from Util.generatePdf import generatePDF
from DataBase.connection import dbAccount
from MyException.ApiException import ValidateError
from Util.BAD_config import msgExcept, SALT_KEY
from flask_jwt_extended import create_access_token
# from Util.validators import Validate


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
            findCpf = [i for i in dbAccount.find({"cpf": self.cpf}, {"cpf"})]
            findEmail = [i for i in dbAccount.find({"email": self.email}, {"email"})]
            findAccount = [i for i in dbAccount.find({"account": self.account}, {"account"})]
            findRandomKey = [i for i in dbAccount.find({"randomKey": self.randomKey}, {"randomKey"})]
            if len(findCpf) < 1 and len(findEmail) < 1 and len(findAccount) < 1 and len(findRandomKey) < 1:
                return ""
            return {"message": "It is not possible to register the account as there is already another one with the same information"}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

    def findOne(self, info=None):
        try:
            user = dbAccount.find_one({"cpf": self.cpf}, {"name", "cpf", "email", "account", "randomKey", "balance"})
            if info:
                return user
            return {"message": user}, 200
        except ValidateError as err:
            return {'message': str(err)}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

    def findOneAndUpdate(self):
        try:
            user = self.findOne()
            if len(user) > 2:
                return {'message': "User not found"}, 400
            if self.password.strip() != "" or self.password is not None:
                passwd = self.password + SALT_KEY
                self.password = hashlib.md5(passwd.encode("UTF-8")).hexdigest()
                dbAccount.update_one({"cpf": self.cpf}, {
                    "$set": {
                        "name": self.fullName or user[0]["message"]["name"],
                        "email": self.email or user[0]["message"]["email"],
                        "password": hashlib.sha256(self.password.encode("UTF-8")).hexdigest(),
                        "dateUpdate": datetime.now().strftime("%d/%m/%Y")
                    }
                }, upsert=True)
            else:
                dbAccount.update_one({"cpf": self.cpf}, {
                    "$set": {
                        "name": self.fullName or user[0]["message"]["name"],
                        "email": self.email or user[0]["message"]["email"],
                        "dateUpdate": datetime.now().strftime("%d/%m/%Y")
                    }
                }, upsert=True)
            return {'message': "Account successfully updated!"}, 200
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

    def findOneLogin(self):
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
            concInfo = f"{user['account']}${user['randomKey']}${user['cpf']}${SALT_KEY}"
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

    @staticmethod
    def accountIsExists(account):
        try:
            findCpf = [i for i in dbAccount.find({"account": account}, {"name", "cpf", "email", "account", "randomKey", "balance"})]
            if len(findCpf) == 1:
                return findCpf[0]
            return None
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500

    def deleteUser(self):
        try:
            user = self.findAccount()
            if user is not None:
                dbAccount.delete_one({'cpf': self.cpf})
                return {"message": "User deleted successfully"}, 200
            return {"message": "User not found"}, 400
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

    def sendPix(self, account, pix):
        try:
            account_sender = self.findOne(True)
            if account_sender["account"] != self.account:
                return {"message": "Your account was not found."}, 400
            account_dst = self.accountIsExists(account)
            if account_sender is not None and account_dst is not None:
                if account_sender["account"] == account_dst["account"]:
                    return {"message": "It is not possible to pix for the same account."}, 400
                if int(account_sender["balance"]) >= pix:
                    value = int(account_sender["balance"]) - pix
                    newValue_dst = int(account_dst["balance"]) + pix
                    try:
                        dbAccount.update_one({"account": account_sender["account"]}, {   # Definindo que a conta que realizou o pix irá diminuir o valor
                            "$set": {
                                "balance": value
                            }}, upsert=True)
                        dbAccount.update_one({"account": account_dst["account"]}, {
                             "$set": {
                                 "balance": newValue_dst
                             }}, upsert=True)
                    except (Exception, ValueError):
                        dbAccount.update_one({"account": account_sender["account"]}, {
                                 "$set": {
                                     "balance": account_sender["balance"]
                                 }}, upsert=True)
                        dbAccount.update_one({"account": account_dst["account"]}, {
                            "$set": {
                                "balance": account_dst["balance"]
                            }}, upsert=True)
                        return {'message': msgExcept}, 500
                else:
                    return {"message": "Insufficient funds"}, 400
                pdf = generatePDF(pix, account_dst["name"], account_dst["account"], account_dst["cpf"],
                                  account_sender["name"], account_sender["account"], account_sender["cpf"])
                return {"message": "Pix performed successfully", "pdf": pdf}, 200
            else:
                return {"message": "Destination account or your account is wrong, please check"}, 400
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 500
