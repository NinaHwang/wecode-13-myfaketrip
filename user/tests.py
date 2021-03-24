from django.test import TestCase, Client
from user.models import User

import bcrypt
import json
# Create your tests here.
class UserTest(TestCase):

    def setUp(self):
        User.objects.create(
            name="Nina",
            password = bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            email = "lodger0812@naver.com",
            location_is_agreed = True,
            promotion_is_agreed = False
            )

    def tearDown(self):
        User.objects.all().delete()

    def test_EmailSignUpView_post_success(self):
        client = Client()
        user = {
            'name'                : 'ChaeYeong',
            'password'            : '12345678',
            'email'               : 'peridot9608@gmail.com',
            'location_is_agreed'  : True,
            'promotion_is_agreed' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code,200)

    def test_EmailSignUpView_post_duplicated_email(self):
        client = Client()
        user = {
            'name'                : 'ChaeYeong',
            'password'            : '12345678',
            'email'               : 'lodger0812@naver.com',
            'location_is_agreed'  : True,
            'promotion_is_agreed' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {"message": "EMAIL_EXISTS"}
        )

    def test_EmailSignUpView_post_invalid_email(self):
        client = Client()
        user = {
            'name'                : 'ChaeYeong',
            'password'            : '12345678',
            'email'               : 'hwangninaagmail.com',
            'location_is_agreed'  : True,
            'promotion_is_agreed' : False
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {"message": "INVALID_EMAIL"}
        )

    def test_EmailSigninView_post_success(self):
        client = Client()
        sign_in_user = {
            "email":"lodger0812@naver.com",
            "password":"12345678"
        }

        response = client.post('/users/signin', json.dumps(sign_in_user), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_EmailSigninView_post_password_incorret(self):
        client = Client()
        sign_in_user = {    
            "email":"lodger0812@naver.com",
            "password":"11111111"
        }
        response = client.post('/users/signin', json.dumps(sign_in_user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
        {"message": "INVALID_PASSWORD"}
        )
    
    def test_EmailSigninView_post_user_not_exists(self):
        client = Client()
        sign_in_user = {
            'email' : 'something@gmail.com',
            'password' : '19960812',
        }
        response = client.post('/users/signin', json.dumps(sign_in_user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
        {"message": "INVALID_USER"}
        )
