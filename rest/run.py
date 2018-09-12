import app
# I created run.py as runner because there were circular reference issues
# w.r.t to python imports if we just use app.py
# https://stackoverflow.com/questions/21766960/operationalerror-no-such-table-in-flask-with-sqlalchemy


import models
import resources
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = app.create_app()
api = Api(app)
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

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
