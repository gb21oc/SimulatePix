"""
-> History DEV:
    -> 10/11/2021: 01h:26
    -> 12/11/2021: 02h:12
"""

import datetime
from flask import Flask
from flask import jsonify
from flask_restful import Api
from utilConfig import SALT_KEY
from Routes.Route import Endpoints
from Util.BLACKLIST import BLACKLIST
from flask_jwt_extended import JWTManager   # pip install Flask-JWT-Extended

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = SALT_KEY
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=1)
api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'Invalid Token'}), 401


if __name__ == '__main__':
    if api:
        Endpoints(api).returnEndpoint()
    app.run(debug=True)
