from flask import Flask
from flask_restful import Api
from Routes.Route import Endpoints


app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    if api:
        Endpoints(api).returnEndpoint()
    app.run(debug=True)
