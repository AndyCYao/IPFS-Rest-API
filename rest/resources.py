from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity,
                                get_raw_jwt)
import requests


IPFS_BASE_URL = "http://localhost:5001"
IPFS_API_VER  = "api/v0"


class UserRegistration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', help='This field cannot be blank', required=True)
    parser.add_argument('password', help='This field cannot be blank', required=True)

    def post(self):
        data = UserRegistration.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresher_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresher_token': refresher_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username', help='This field cannot be blank', required=True)
    parser.add_argument('password', help='This field cannot be blank', required=True)

    def post(self):
        data = UserRegistration.parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresher_token = create_refresh_token(identity=data['username'])            
            return {'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresher_token': refresher_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {'answer': 42}


class AddFile(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('fileName', help='Required, File Name', required=True)

    @jwt_required
    def post(self):
        '''connects to /api/v0/add
        args [file] required
        '''
        data = AddFile.parser.parse_args()
        files = {'files': (data['fileName'], open(data["fileName"], 'rb'))}

        response = requests.post('{}/{}/add'.format(IPFS_BASE_URL, IPFS_API_VER),
                                files=files)
        print(response)
        print(response.json())
        if(response.status_code == 200):
            responseJson = response.json()
            responseHash = responseJson["Hash"]
            # Response from IPFS
            return {
                'success': True,
                'error': 0,
                'fileUrl': "{}/{}".format(IPFS_BASE_URL, responseHash),
                'fileHash': responseHash
            }, 200
        else:
            return {'message': 'could not add file'}, 500


class DeleteFile(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('file', help='Required, Content Address Of the File', required=True)

    @jwt_required
    def post(self):
        '''connects to /api/v0/pin/rm
        args [file] required
        since IPFS is permanent, this will unpin the file and call garbage collection
        '''
        # data  = flask_request.get_json()
        data = DeleteFile.parser.parse_args()
        response = requests.post('{}/{}/pin/rm?arg={}'.format(IPFS_BASE_URL, IPFS_API_VER, data['file']))
        print(response.status_code)
        print(response.json())
        if response.status_code == 200 and self.garbageCollect() == 200:
            return {
                'success': True,
                'error': ''
            }, 200
        else:
            return {'message': 'could not delete file'}, 500
        
    def garbageCollect(self):
        '''performs garbage colection
        '''
        response = requests.post('{}/{}/repo/gc'.format(IPFS_BASE_URL, IPFS_API_VER))
        return response.status_code

