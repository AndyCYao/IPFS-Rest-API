
import unittest
import app as app_module
from models import db
import json

class FlaskTestCase(unittest.TestCase):
    def setUp(self):

        self.app = app_module.create_app('config.TestingConfig')
        self.client = self.app.test_client()

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            # user_datastore.create_user(user='test', password=encrypt_password('test'))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _post(self, route, data=None, content_type=None, follow_redirects=True, headers=None):
        content_type = content_type or 'application/x-www-form-urlencoded'
        return self.client.post(route, data=data, follow_redirects=follow_redirects, content_type=content_type,
                                headers=headers)

    def _login(self, user=None, password=None):
        user = user or 'test'
        password = password or 'test'
        data = {
            'user': user,
            'password': password,
        }
        return self._post('/login', data=data, follow_redirects=False)


class APITest(FlaskTestCase):
    # def _auth(self, username=None, password=None):
    #     username = username or 'test'
    #     password = password or 'test'
    #     rv = self._post('/api/v1/auth',
    #                     data=json.dumps({'username': username, 'password': password})
    #                     )
    #     return json.loads(rv.data.decode())

    def _get(self, route, data=None, content_type=None, follow_redirects=True, headers=None):
        content_type = content_type or 'application/json'
        if hasattr(self, 'token'):
            headers = headers or {'Authorization': 'JWT ' + self.token}
        return self.client.get(route, data=data, follow_redirects=follow_redirects, content_type=content_type,
                               headers=headers)

    def _post(self, route, data=None, content_type=None, follow_redirects=True, headers=None):
        content_type = content_type or 'application/json'
        if hasattr(self, 'token'):
            headers = headers or {'Authorization': 'Bearer ' + self.token}
        return self.client.post(route, data=data, follow_redirects=follow_redirects, content_type=content_type,
                                headers=headers)

    def test_login(self):
        '''Given When Then'''
        user     = 'test_test'
        password = 'test_pass'
        login_resp = self._login()
        print(login_resp.status_code)
        print(login_resp)
        return True

    def test_auth(self):
        return self.assertTrue("Hello", "Hello")
        # Get auth token with invalid credentials
        # auth_resp = self._auth('not', 'existing')
        # self.assertEqual(401, auth_resp['status_code'])

        # # Get auth token with valid credentials
        # auth_resp = self._auth('test', 'test')
        # self.assertIn(u'access_token', auth_resp)

        # self.token = auth_resp['access_token']

        # # Get empty collection
        # rv = self._get('/api/v1/protected_stuff')
        # self.assertEqual(200, rv.status_code)
        # data = json.loads(rv.data.decode())
        # self.assertEqual(data['num_results'], 0)

        # # Post object to collection
        # rv = self._post('/api/v1/protected_stuff', data=json.dumps({'data1': 1337, 'data2': 'Test'}))
        # self.assertEqual(201, rv.status_code)

        # # Get collection if new object
        # rv = self._get('/api/v1/protected_stuff')
        # data = json.loads(rv.data.decode())
        # self.assertEqual(data['num_results'], 1)

        # # Post another object and get it back
        # rv = self._post('/api/v1/protected_stuff', data=json.dumps({'data1': 2, 'data2': ''}))
        # self.assertEqual(201, rv.status_code)
        # rv = self._get('/api/v1/protected_stuff/2')
        # data = json.loads(rv.data.decode())
        # self.assertEqual(data['data1'], 2)

if __name__ == '__main__':
    unittest.main()
