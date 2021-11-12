import hashlib
import re

from flask import request
from utilConfig import SALT_KEY

from Util.BAD_config import msgExcept
from MyException.ApiException import ValidateError


class Validate:
    # error = []

    def __init__(self, cpf=None, email=None, password=None, fullName=None, account=None, randomKey=None, secure=None):
        self.error = []
        self.fullname = fullName
        self.cpf = cpf
        self.email = email
        self.password = password
        self.randomKey = randomKey
        self.account = account
        self.secure = secure

    def valida(self):
        if self.cpf is not None:
            self.validateCpf()
        if self.email is not None:
            self.validateEmail()
        if self.password is not None:
            self.validatePassword()
        if self.fullname is not None:
            self.validateName()
        if self.fullname is not None:
            self.validateSecureToken()
        if len(self.error) < 1:
            return ""
        else:
            raise ValidateError(f"An error has occurred: {str(self.error)}")

    def validateCpf(self):
        try:
            if self.cpf is None:
                self.error.append("CPF is not None")

            if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', self.cpf):
                self.error.append("CPF is not format corret")

            # Obtém apenas os números do CPF, ignorando pontuações
            numbers = [int(digit) for digit in self.cpf if digit.isdigit()]

            # Verifica se o CPF possui 11 números ou se todos são iguais:
            if len(numbers) != 11 or len(set(numbers)) == 1:
                self.error.append("CPF does not have 11 numbers")

            # Validação do primeiro dígito verificador:
            sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
            expected_digit = (sum_of_products * 10 % 11) % 10
            if numbers[9] != expected_digit:
                self.error.append("CPF is not correct")

            # Validação do segundo dígito verificador:
            sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
            expected_digit = (sum_of_products * 10 % 11) % 10
            if numbers[10] != expected_digit:
                self.error.append("CPF is not correct")

        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 400

    def validateEmail(self):
        try:
            if self.email is None:
                self.error.append("E-MAIL is not None")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.fullmatch(regex, self.email.strip()):
                return True
            else:
                self.error.append("E-MAIl not format correct")
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 400

    def validatePassword(self):
        try:
            if self.password is None:
                self.error.append("PASSWORD is not None")
            if len(self.password) < 8:
                self.error.append("PASSWORD must be greater than 8 digits")
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 400

    def validateName(self):
        try:
            if self.fullname is None:
                self.error.append("NAME is not None")
            if len(self.fullname) < 3:
                self.error.append("NAME must be greater than 3 digits")
            for i in self.fullname:
                if i.isnumeric():
                    self.error.append("NAME name cannot contain numbers")
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 400

    def validateSecureToken(self):
        try:
            secure = request.headers["secureToken"]
            if secure is None or secure.strip() == "":
                self.error.append("Token cannot be empty")
            concInfo = f"{self.account}${self.randomKey}${self.cpf}${SALT_KEY}"
            updateToken = hashlib.sha256(concInfo.encode("UTF-8")).hexdigest()
            if updateToken != secure:
                self.error.append("Invalid Token")
        except (Exception, ValueError, IndexError) as err:
            print(str(err))
            return {'message': msgExcept}, 400
