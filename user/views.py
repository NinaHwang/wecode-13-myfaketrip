import os
import json
import bcrypt
import re
import jwt
import my_settings
import utils
import requests

from django.views           import View
from user.models            import User
from django.http            import JsonResponse

# Create your views here.
def print_this():
    print('this')

class EmailSignUpView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not (re.search(regex, data['email'])):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EMAIL_EXISTS"}, status=400)

            password       = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            User(
                name                = data['name'],
                password            = password_crypt,
                email               = data['email'],
                location_is_agreed  = data['location_is_agreed'],
                promotion_is_agreed = data['promotion_is_agreed'],
            ).save()

            return JsonResponse({"message": "SIGNUP_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)


class EmailSignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])

            if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                key       = my_settings.SECRET.get('SECRET_KEY')
                algorithm = my_settings.SECRET.get('JWT_ALGORITHM')
                token     = jwt.encode({'user' : user.id},key, algorithm = algorithm).decode('UTF-8')
                return JsonResponse({"token": token, "message": "SIGNIN_SUCCESS", "name" : user.name}, status=200)

            else:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)


class KakaoSignInView(View): 
    def get(self, request):

        access_token = request.headers.get('Authorization', None)
        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization':f'Bearer {access_token}'
        }
        
        kakao_response = requests.post(url, headers = headers)

        data = kakao_response.json()
        data_kakao = data['kakao_account']
        user_email = data_kakao['email']
        social_id = data['id']

        try:
            if not User.objects.filter(email = user_email).exists():
                User.objects.create(
                    name = user_email,
                    email = user_email,
                    social_id = social_id,
                    password  = 0000,
                    location_is_agreed  = False,
                    promotion_is_agreed = False
                )

            user = User.objects.get(social_id = social_id)
            
            key        = my_settings.SECRET.get('SECRET_KEY')
            algorithm = my_settings.SECRET.get('JWT_ALGORITHM')
            token     = jwt.encode({'user' : user.id},key, algorithm = algorithm).decode('UTF-8')
            
            
            return JsonResponse(
                {"token": token, "message": "SIGNIN_SUCCESS", "name" : user.name}, status=200
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)
