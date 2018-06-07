import unittest
from app.views import app
import json
from flask_login import current_user
from app.dbmodel.dbmodels import users

class TestClass(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
    #get all requests check
    def test_requests(self):
        response = {'request_type':'car repair', 'desscription':'faulty engine'}
        
        my_request = self.tester.get('api/v1/requests', content_type = 'application/json')
        request_resp = json.dumps(my_request.data.decode())
        self.assertEqual(response, request_resp['all_requests'])
    
    #get all requests status code check
    def test_all_requests(self):
        response = self.tester.get('/api/v1/requests')
        self.assertEqual(response.status_code, 200)

    #checking that users can add requests
    def test_add_req(self):
        dta = {'request_type':'phone repair', 'desscription':
              'cracked screen'}
        response = self.tester.post('/api/v1/requests', content_type = 'application/json', 
                                     data = json.dumps(dta))

        self.assertEqual(response.status_code, 200)

    #check that incorrect request is not posted.
    def test_incorrect_req(self):
        response = self.tester.post('/api/v1/requests')
        self.assertEqual(response.status_code, 400)

    #check invalid request modification.
    def test_edit_req(self):
        response = self.tester.put('/api/v1/requests/<int:requestid>', content_type = 'application/json')
        self.assertEqual(response.status_code, 405)

    #testing user signup
    def test_signup(self):
        with self.tester:
            response = self.tester.post('/api/v1/Signup',
            data=json.dumps(dict(email='laptop@gmail.com',username='laptop', 
                              user_password='123',confirm_password='123')), 
                              content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertIn(b'new user created', response.data)
   
    #valid signup test status_code
    def test_signup_code(self):
        response = self.tester.post('/api/v1/Signup', data=json.dumps(dict(email='laptop@gmail.com',
                                  username='laptop',user_password='123',confirm_password='123')), 
                                  content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)

    #unmatching passwords test
    def test_variance(self):
        response = self.tester.post('/api/v1/Signup',content_type = 'application/json')
        self.assertTrue('Unmatching passwords. Please try again.', response.data)
        

