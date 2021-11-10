import re
from Util.config import msgExcept


class Validate:
    error = []

    def __init__(self, cpf=None, email=None, password=None, fullName=None):
        self.fullname = fullName
        self.cpf = cpf
        self.email = email
        self.password = password

    def valida(self):
        if self.cpf is not None:
            self.validateCpf()
        if self.email is not None:
            self.validateEmail()
        if self.password is not None:
            self.validadePassword()
        if self.fullname is not None:
            self.validadeName()
        if len(self.error) < 1:
            return ""
        else:
            return self.error

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
            if re.fullmatch(regex, self.email):
                return True
            else:
                self.error.append("E-MAIl not format correct")
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 400

    def validadePassword(self):
        try:
            if self.password is None:
                self.error.append("PASSWORD is not None")
            if len(self.password) < 8:
                self.error.append("PASSWORD must be greater than 8 digits")
        except (Exception, ValueError, IndexError):
            return {'message': msgExcept}, 400

    def validadeName(self):
        msg = "NAME is not valid"
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
