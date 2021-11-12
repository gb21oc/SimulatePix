import socket

# System Info
ip = socket.gethostbyname(socket.gethostname())
# KEYS
SALT_KEY = "FR0jzQjSJ|_v!E-=9K`gGt{Fi*|KUacqKv2K>1CUS/eDJ}w{m9aiD,E9(ckK#LJt')"
SEND_GRID_KEY = ""
# MSG Except
msgExcept = "An internal error has occurred please try again!!"
# Config E-mail
bodyLogin = """
<html>
        <head><meta charset='utg-8'></head>
        <body>
            <h1> Login attempt notification </h1>
            <p> Hello @name, </p>
            <p> Date: @date </p>
            <p> IP address: @ip, </p>
            <p> 
                If you do not recognize this login attempt, please change your login password as soon as possible.. 
            </p>
        </body>
    </html>
"""
body = """
<html>
        <head><meta charset='utg-8'></head>
        <body>
            <h1> Welcome to Giants @name </h1>
            <p> 
                Thank you for creating an account with us. Enjoy your advantages well!!!
                Your information:
                <p> Name: <strong> @name </strong> </p>
                <p> E-mail: <strong> @email </strong> </p>
                <p> Password: <strong> @password </strong> </p>
                <p> Account: <strong> @account </strong> </p>
                <br><br><br><br>
                <span> Thank you and have a nice day! </span>
            </p>
        </body>
    </html>
"""