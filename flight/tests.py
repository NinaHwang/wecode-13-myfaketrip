import unittest
import json
import datetime

from django.test            import TestCase, Client
from django.core.exceptions import ImproperlyConfigured

from flight.models     import Flight, FlightWeekday, Airline, Airport

class flight_list_get_Test(TestCase):
    maxDiff = None
    def setUp(self):
        Airline.objects.create(
            id=1,
            name='airline1',
            logo_url='www.url.com'
        )
        Airport.objects.create(
            id=1,
            name='airport1',
            eng_name='airport1'
        )
        Flight.objects.create(
            id=1,
            flightid='flight1',
            airport_depart_id = 1,
            airport_arrive_id = 1,
            depart_time="11:00:00",
            arrive_time="12:00:00",
            start_date="2020-11-18",
            end_date="2020-11-19",
            airline_id=1,
            remain_seats=10,
            basic_price=300000.00,
            seat_class='flight1'
        )
        FlightWeekday.objects.create(
            id=1,
            flight_id=1,
            weekday='flightweekday',
            date="2020-11-18"
        )

    def tearDown(self):
        Airport.objects.all().delete()
        Airline.objects.all().delete()
        Flight.objects.all().delete()
        FlightWeekday.objects.all().delete()

    def test_flight_list_get_success(self):
        client = Client()
        response = client.get('/air?go=go&airport_depart=airport1&airport_arrive=airport1&start_date=2020-11-18&airline_list=airline1&seat_class=flight1', content_type = 'application/json')
        self.assertEqual(response.json(),
            {
    "message": "SUCCESS!",
    "start_flight": [
        {
            "id": 1,
            "airport_depart": "airport1",
            "airport_arrive": "airport1",
            "depart_date": "2020-11-18",
            "depart_weekday": "flightweekday",
            "flightid": "flight1",
            "airport_depart_eng": "airport1",
            "airport_arrive_eng": "airport1",
            "depart_time": "11:00:00",
            "arrive_time": "12:00:00",
            "airline": "airline1",
            "airline_url": "www.url.com",
            "remain_seats": 10,
            "basic_price": "300000.00",
            "seat_class": "flight1"
        }
    ]
}
        )
        self.assertEqual(response.status_code, 200)

    def test_flight_list_get_not_found(self):
        client = Client()
        response = client.get('/air?airport_arrive=김포&depart_date=2020-11-18&airline_list=airline1&seat_class=flight1', content_type = 'application/json')
        self.assertEqual(response.json(),{"message":"Not Found URL"})
        self.assertEqual(response.status_code, 400)