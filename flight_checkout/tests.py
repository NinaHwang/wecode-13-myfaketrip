import unittest
import datetime
import bcrypt
import json
import jwt

from django.test            import TestCase, Client
from unittest.mock          import patch, MagicMock

from my_settings            import SECRET
from user.models            import User
from flight.models          import Flight, FlightWeekday, Airline, Airport
from flight_checkout.models import BookingInfo


class flight_booking(TestCase):
    def setUp(self):
        password       = bytes('1234', 'utf-8')
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        User.objects.create(
            id                  = 1,
            name                = "a",
            password            = password_crypt,
            email               = "thisisa@gmail.com",
            location_is_agreed  = True,
            promotion_is_agreed = True,
        )
        Airline.objects.create(
            id       = 1,
            name     = 'airline1',
            logo_url = 'www.url.com'
        )
        Airport.objects.create(
            id       = 1,
            name     = 'airport1',
            eng_name = 'airport1'
        )
        Flight.objects.create(
            id                = 1,
            flightid          = 'flight1',
            airport_depart_id = 1,
            airport_arrive_id = 1,
            depart_time       = "11:00:00",
            arrive_time       = "12:00:00",
            start_date        = "2020-11-18",
            end_date          = "2020-11-19",
            airline_id        = 1,
            remain_seats      = 10,
            basic_price       = 300000.00,
            seat_class        = 'flight1'
        )
        BookingInfo.objects.create(
            user_id         = 1,
            start_flight_id = 1,
            end_flight_id   = 1,
            start_date      = "2020-11-18",
            end_date        = "2020-11-19",
            total_people    = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        BookingInfo.objects.all().delete()
        Airport.objects.all().delete()
        Airline.objects.all().delete()
        Flight.objects.all().delete()

    def test_flight_booking_list_post_success(self):
        client = Client()
        test = {"email" : "thisisa@gmail.com", "password" : "1234"}
        response = client.post('/users/signin', json.dumps(test), content_type="application/json")
        access_token = response.json()['token']
        booking = {
            "start_flight_id" : 1,
            "end_flight_id"   : 1,
            "start_date"      : "2020-11-18",
            "end_date"        : "2020-11-19",
            "total_people"    : 1
        }
        response = client.post('/air/booking', json.dumps(booking), content_type='application/json', **{'HTTP_AUTHORIZATION': access_token})
        self.assertEqual(response.json(),{"message":"SUCCESS!"})
        self.assertEqual(response.status_code, 201)

    def test_flight_booking_list_post_key_error(self):
        client = Client()
        test = {"email" : "thisisa@gmail.com", "password" : "1234"}
        response = client.post('/users/signin', json.dumps(test), content_type="application/json")
        access_token = response.json()['token']
        booking = {
            "start_flight_ids" : 1,
            "end_flight_id"    : 1,
            "start_date"       : "2020-11-18",
            "end_date"         : "2020-11-19",
            "total_people"     : 1
        }
        response = client.get('/air/booking', json.dumps(booking), content_type = 'application/json', **{'HTTP_AUTHORIZATION': access_token})
        self.assertEqual(response.json(),{"message":"KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    def test_flight_booking_list_post_does_not_exist_error(self):
        client = Client()
        test = {"email" : "thisisa@gmail.com", "password" : "1234"}
        response = client.post('/users/signin', json.dumps(test), content_type="application/json")
        access_token = response.json()['token']
        booking = {
            "start_flight_id"  : 2,
            "end_flight_id"    : 1,
            "start_date"       : "2020-11-18",
            "end_date"         : "2020-11-19",
            "total_people"     : 1
        }
        response = client.get('/air/booking', json.dumps(booking), content_type = 'application/json', **{'HTTP_AUTHORIZATION': access_token})
        self.assertEqual(response.json(),{"message":"Object_DoesNotExist"})
        self.assertEqual(response.status_code, 400)

    def test_flight_booking_list_get_success(self):
        client = Client()
        test = {"email" : "thisisa@gmail.com", "password" : "1234"}
        response = client.post('/users/signin', json.dumps(test), content_type="application/json")
        access_token = response.json()['token']
        response = client.get('/air/booking', content_type = 'application/json', **{'HTTP_AUTHORIZATION': access_token})
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS!",
                "start_flight" : [
                    {
                        "depart_airport_name"     : "airport1",
                        "arrive_airport_name"     : "airport1",
                        "depart_airport_eng_name" : "airport1",
                        "arrive_airport_eng_name" : "airport1",
                        "depart_date"             : "2020-11-18",
                        "airline_name"            : "airline1",
                        "airline_logo"            : "www.url.com",
                        "seat_class"              : "flight1",
                        'total_people'            : 1
                    }
            ],
                "end_flight" : [
                    {
                        "depart_airport_name"     : "airport1",
                        "arrive_airport_name"     : "airport1",
                        "depart_airport_eng_name" : "airport1",
                        "arrive_airport_eng_name" : "airport1",
                        "depart_date"             : "2020-11-19",
                        "airline_name"            : "airline1",
                        "airline_logo"            : "www.url.com",
                        "seat_class"              : "flight1",
                        'total_people'            : 1
                    }
            ]
    }
        )
        self.assertEqual(response.status_code, 200) 