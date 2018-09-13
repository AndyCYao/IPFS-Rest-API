import app
# I created run.py as runner because there were circular reference issues
# w.r.t to python imports if we just use app.py
# https://stackoverflow.com/questions/21766960/operationalerror-no-such-table-in-flask-with-sqlalchemy


import models
# import resources
# from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = app.create_app()

if __name__ == '__main__':
    # for rule in app.url_map.iter_rules():
    #     print(rule)
    app.run(host='0.0.0.0', port=8081, debug=True)

    # curl -F "testImg=@blockchain.png" 127.0.0.1:5001/api/v0/add