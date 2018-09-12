from flask import Flask, request as flask_request, Response, abort
import requests
import json
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

IPFS_BASE_URL = "http://localhost:5001"
IPFS_API_VER  = "api/v0"

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


import models
import resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

@app.route('/')
def index():
    return 'Hello'


@app.route("/add", methods=['POST'])
def add():
    '''connects to /api/v0/add
    args [file] required
    '''
    data        = flask_request.get_json()
    sourceFile  = data["files"]
    files = {'files': (sourceFile, open(sourceFile, 'rb'))}

    response = requests.post('{}/{}/add'.format(IPFS_BASE_URL, IPFS_API_VER),
                                        files=files)
    print(response)
    print(response.json())
    if(response.status_code == 200):
        responseJson = response.json()
        responseHash = responseJson["Hash"]
        # Response from IPFS
        payload = {
            "success": True,
            "error": 0,
            "fileUrl": "{}/{}".format(IPFS_BASE_URL, responseHash),
            "fileHash": responseHash
        }
        return Response(json.dumps(payload), status=200,
                        mimetype='application/json')
    else:
        return abort(500)


def _garbageCollect():
    '''performs garbage colection
    '''
    response = requests.post('{}/{}/repo/gc'.format(IPFS_BASE_URL, IPFS_API_VER))
    return response.status_code


@app.route("/delete", methods=['POST'])
def delete():
    '''connects to /api/v0/pin/rm
    args [files] required
    since IPFS is permanent, this will unpin the file and call garbage collection
    '''
    data  = flask_request.get_json()
    file  = data["files"]
    response = requests.post('{}/{}/pin/rm?arg={}'.format(IPFS_BASE_URL, IPFS_API_VER, file))
    print(response.status_code)
    print(response.json())
    if response.status_code == 200 and _garbageCollect() == 200:
        payload = {
            "success": True,
            "error": ""
        }
        return Response(json.dumps(payload), status=200, 
                        mimetype="application/json")
    else:
        return abort(500)


@app.errorhandler(500)
def internal_error(error):
    return json.dumps({"error": "Error Handling Data"})
