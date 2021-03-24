from django.test    import TestCase, Client
from datetime       import timedelta, datetime
from unittest       import mock
from review.models  import Review
from hotel.models   import Hotel, Region, City
from user.models    import User

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

        User.objects.create(
            id = 1,
            name = 'Nina',
            email='hwangninaa@gmail.com',
            password='12345678',
            location_is_agreed=True,
            promotion_is_agreed=True
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_HotelReviewView_get_success(self):

        Review.objects.create(
            id = 1,
            hotel = Hotel.objects.get(id=1),
            user =User.objects.get(id=1),
            rating = 10,
            title = 'Good',
            content = 'Good' 
            )

        client = Client()
        response = client.get('/reviews/1')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
        {'review_list':[{
            "hotel": 1,
            "user": 1,
            "rating": 10,
            "created_at": Review.objects.get(id=1).created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "title": "Good",
            "content": "Good"
        }]})

    def test_HotelReviewView_get_return_nothing(self):
        
        client = Client()
        response = client.get('/reviews/3')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'review_list':[
        ]}
        )