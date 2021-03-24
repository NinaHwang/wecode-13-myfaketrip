from django.test         import TestCase, Client
from datetime            import timedelta, datetime
from unittest            import mock
from review.models       import Review
from hotel.models        import Hotel, Region, City, HotelOption, Option
from user.models         import User
from hotel_booking.models import HotelBooking, BookingInfo, WishList

import os
import bcrypt
import re
import jwt
import my_settings
import utils

import json

# Create your tests here.
class UserTest(TestCase):
    maxDiff = None
    def setUp(self):

        Region.objects.create(
            id = 1,
            name='Korea'
        )

        City.objects.create(
            id=1,
            region = Region.objects.get(id=1),
            name='Seoul'
        )

        Hotel.objects.create(
            id = 1,
            name='Lotte Hotel',
            thumbnail_url='lotte.jpg',
            description='great hotel',
            basic_price =333000.00,
            checkin_time='14:00:00',
            checkout_time='14:00:00',
            city = City.objects.get(id=1),
            location='Seoul, Korea',
            star=5
        )

        Option.objects.create(
            id = 1,
            name = 'deluxe'
        )

        HotelOption.objects.create(
            id = 1,
            hotel = Hotel.objects.get(id=1),
            option = Option.objects.get(id=1),
            additional_price = 15000.00
        )

        User.objects.create(
            id=1,
            name="Nina",
            password = bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            email = "lodger0812@naver.com",
            location_is_agreed = True,
            promotion_is_agreed = False
            )

    def tearDown(self):

        Region.objects.all().delete()
        City.objects.all().delete()
        Hotel.objects.all().delete()
        HotelOption.objects.all().delete()
        User.objects.all().delete()

    def test_HotelBookingView_post_success(self):
        
        client = Client()
        
        sign_in_user = {
            "email":"lodger0812@naver.com",
            "password":"12345678"
        }
        

        sign_in_response = client.post('/users/signin', json.dumps(sign_in_user), content_type='application/json')
        token          = sign_in_response.json()["token"]
        header         = {"HTTP_Authorization" : token}

        booking_info = {
            "hotel":1,
            "option":1,
            "name":"Nina",
            "sex":"Femail",
            "birth":'1996-08-12',
            "checkin_date":"2020-11-12",
            "checkout_date":"2020-11-14",
            "arrival_time":"14:00:00",
            "mobile":"010-8831-7265",
            "total_people":1
        }

        booking_response = client.post('/accommodations/booking',json.dumps(booking_info), **header, content_type = 'application/json')

        self.assertEqual(booking_response.status_code,201)

    def test_HotelBookingView_post_key_error(self):
        client = Client()
        
        sign_in_user = {
            "email":"lodger0812@naver.com",
            "password":"12345678"
        }
        

        sign_in_response = client.post('/users/signin', json.dumps(sign_in_user), content_type='application/json')
        token          = sign_in_response.json()["token"]
        header         = {"HTTP_Authorization" : token}

        booking_info = {
            "hotel":1,
            "option":1,
            "sex":"Femail",
            "birth":'1996-08-12',
            "checkin_date":"2020-11-12",
            "checkout_date":"2020-11-14",
            "arrival_time":"14:00:00",
            "mobile":"010-8831-7265",
            "total_people":1
        }

        booking_response = client.post('/accommodations/booking',json.dumps(booking_info), **header, content_type = 'application/json')

        self.assertEqual(booking_response.status_code,400)
        self.assertEqual(booking_response.json(),
         {'message': 'KEY_ERROR'}
        )
