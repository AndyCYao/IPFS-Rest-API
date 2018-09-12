from flask import Flask, request as flask_request, Response, abort
# import requests
# import json
# from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# from flask_restful import Api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    return app

# app = Flask(__name__)
# # api = Api(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'some-secret-string'
# app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# jwt = JWTManager(app)

# db = SQLAlchemy(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()


# import models
# import resources

# api.add_resource(resources.UserRegistration, '/registration')
# api.add_resource(resources.UserLogin, '/login')
# api.add_resource(resources.UserLogoutAccess, '/logout/access')
# api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
# api.add_resource(resources.TokenRefresh, '/token/refresh')
# api.add_resource(resources.AllUsers, '/users')
# api.add_resource(resources.SecretResource, '/secret')
# api.add_resource(resources.AddFile, '/add')
# api.add_resource(resources.DeleteFile, '/delete')

# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return models.RevokedTokenModel.is_jti_blacklisted(jti)


# @app.route('/')
# def index():
#     return 'Hello'
