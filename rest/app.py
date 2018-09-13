from flask import Flask, request as flask_request, Response, Blueprint
import resources
import models
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Using flask factory app creation
def create_app(environment='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(environment)

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(resources.UserRegistration, '/registration')
    api.add_resource(resources.UserLogin, '/login')
    api.add_resource(resources.UserLogoutAccess, '/logout/access')
    api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(resources.TokenRefresh, '/token/refresh')
    api.add_resource(resources.AllUsers, '/users')
    api.add_resource(resources.SecretResource, '/secret')
    api.add_resource(resources.AddFile, '/add')
    api.add_resource(resources.DeleteFile, '/delete')
    
    jwt = JWTManager(app)

    db = models.db
    db.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedTokenModel.is_jti_blacklisted(jti)
    
    @app.before_first_request
    def create_tables():
        with app.app_context():
            db.create_all()
    
    @app.route('/')
    def index():
        return 'Hello'

    app.register_blueprint(api_bp)
    return app