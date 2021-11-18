from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from utilConfig import body, bodyLogin, SEND_GRID_KEY, ip


class SendEmail:
    def __init__(self, email=None, password=None, fullName=None, account=None, ip=None):
        self.email = email
        self.account = account
        self.fullname = fullName
        self.password = password
        self.ip = ip

    def send(self, type, subject):
        msg = ""
        if type == "Create":
            msg = Mail(
                from_email="roboGb021@gmail.com",
                to_emails=self.email,
                subject=subject,
                html_content=body.replace("@name", self.fullname).replace("@email", self.email).replace
                ("@password", self.password).replace("@account", self.account)
            )
        if type == "Login":
            dateNow = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            msg = Mail(
                from_email="roboGb021@gmail.com",
                to_emails=self.email,
                subject=subject,
                html_content=bodyLogin.replace("@name", self.fullname).replace("@date", dateNow).replace("@ip", self.ip)
            )
        try:
            sg = SendGridAPIClient(SEND_GRID_KEY)
            sg.send(msg)
        except (Exception, IndexError, ValueError) as err:
            raise Exception("There was an error sending the E-mail")
