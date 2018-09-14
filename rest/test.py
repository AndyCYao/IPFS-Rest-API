
import unittest
import app as app_module
from models import db
import json

class FlaskFixture(unittest.TestCase):
    
    def setUp(self):
        self.app = app_module.create_app('config.TestingConfig')
        # for rule in self.app.url_map.iter_rules():
        #     print(rule)
        self.client = self.app.test_client()
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            # user_datastore.create_user(user='test', password=encrypt_password('test'))
            # db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _get(self, route, data=None, content_type='application/json', follow_redirects=False, headers=None, token=None):

        if token:
            headers = {'Authorization': 'Bearer ' + token}
        return self.client.get(route, data=data, follow_redirects=follow_redirects, content_type=content_type, headers=headers)

    def _post(self, route, data=None, content_type='application/json', follow_redirects=False, headers=None, token=None):

        if token:
            headers = {'Authorization': 'Bearer ' + token}
        return self.client.post(route, data=data, follow_redirects=follow_redirects, content_type=content_type, headers=headers)

    def get_mock_user(self):
        '''mock a user for testing purpose'''
        _user = 'zb'
        _pass = 'andy'
        res = self._post('/registration', data=json.dumps({"username": _user, "password": _pass}))
        _decode_res = json.loads(res.data.decode())
        _token = _decode_res['access_token']
        return _user, _pass, _token

class APITest(FlaskFixture):

    def test_register(self):
        '''test register an user, status should be 200, and returns an access token'''
        res = self._post('/registration', data=json.dumps({"username": "test", "password": "test"}))
        _decode_res = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertIn(u'access_token', _decode_res)

    def test_home_hello(self):
        '''test pinging the root endpoint'''
        res = self._get('/')
        return self.assertEqual(res.data.decode(), 'Hello')
    
    def test_login(self):
        '''test login'''
        self._post('/registration', data=json.dumps({"username": "test", "password": "test"}))
        res = self._post('/login', data=json.dumps({"username": "test", "password": "test"}))
        _decode_res = json.loads(res.data.decode())
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(u'access_token', _decode_res, "should return access token")
        self.assertIn(u'refresher_token', _decode_res, "should return refresher token")
        
    def test_protected_data(self):
        '''testing the secret end point, which needs JWT token'''
        res = self._get('/secret')
        _decode_res = json.loads(res.data.decode())
        self.assertIn(u'Missing Authorization', _decode_res['msg'], "restricted endpoint")
        
        _user, _pass, _token = self.get_mock_user()
        res = self._get('/secret', token=_token)
        _decode_res = json.loads(res.data.decode())
        self.assertEqual(42, _decode_res['answer'], "restricted endpoint with access_token")


class AddDeleteTest(FlaskFixture):

    def _post(self, route, data=None, content_type='application/json', follow_redirects=False, headers=None, token=None):
        if token:
            headers = {'Authorization': 'Bearer ' + token}
        return self.client.post(route, data=data, content_type=content_type, headers=headers)

    def test_upload_file(self):
        '''testing the add end point, needs JWT token'''

        res = self._post('/add', content_type='multipart/form-data')
        _decode_res = json.loads(res.data.decode())
        self.assertIn(u'Missing Authorization', _decode_res['msg'], "restricted endpoint")
                 
        # Testing if uploaded with 200 status code, and should have hash code

        _file = {
            'fileObj': (open('demoText.txt', 'rb'), 'demoText.txt'),
        }
        _user, _pass, _token = self.get_mock_user()
        res = self._post('/add', data=_file, token=_token, content_type='multipart/form-data')
        _decode_res = json.loads(res.data.decode())
        self.assertEqual(200, res.status_code, "successfully uploaded file")
        # Should return file hash, and fileUrl
        self.assertIn(u'fileUrl', _decode_res, 'Response should include file url')
        self.assertIn(u'fileHash', _decode_res,'Response should include file hash')

    def test_delete_file(self):
        '''testing the delete endpoint, needs JWT Token'''
        _user, _pass, _token = self.get_mock_user()
        _file = {'fileObj': open('demoText2.txt', 'rb')}
        res = self._post('/add', data=_file, token=_token)
        _decode_res = json.loads(res.data.decode())
        _fileHash = _decode_res['fileHash']
        # Test
        _file = {'file': _fileHash}
        res = self._post('/delete', data=_file, token=_token)
        _decode_res = json.loads(res.data.decode())
        self.assertEqual(200, res.status_code, 'successfully deleted file')
        self.assertIn(u'success', _decode_res)


if __name__ == '__main__':
    unittest.main()
