import json
from django.test import TestCase, Client
from hotel.models import Region, City, Hotel, HotelImage, Convenience, HotelConvenience
# Create your tests here.

class HotelTest(TestCase):

    maxDiff = None
    
    def setUp(self):
        client = Client()
        Region.objects.create(
            id = 1,
            name = 'Seoul'
        )
        City.objects.create(
            id = 1,
            region = Region.objects.get(id=1),
            name = 'Gangnam'
        )

        Hotel.objects.create(
            id = 1,
            name = 'Lotte Hotel',
            description = 'Ocean View',
            basic_price = 333000.00,
            checkin_time = '14:00:00',
            checkout_time = '12:00:00',
            city = City.objects.get(id=1),
            location = 'Somewhere only we know',
            star = 5,
            thumbnail_url = 'https://www.lottehotel.com/content/dam/lotte-hotel/lotte/seoul/main/181023-1-2000-mai-LTSE.jpg.thumb.768.768.jpg'
        )

        HotelImage.objects.create(
            id = 1,
            hotel_id = 1,
            image_url = 'this_is_an_image.jpg'
        )

        Convenience.objects.create(
            id = 1,
            name = 'something good',
            icon_url = 'icon.jpg'
        )

        HotelConvenience.objects.create(
            id = 1,
            hotel_id = 1,
            convenience_id = 1
        )

    def tearDown(self):
        Region.objects.all().delete()
        City.objects.all().delete()
        Hotel.objects.all().delete()

    def test_HotelListView_get_success(self):
        client = Client()
        response = self.client.get('/accommodations/hotels')
        self.assertEqual(response.json(),
             {'hotels': [{'id': 1,
              'name': 'Lotte Hotel',
              'price': '333000.00',
              'star': 5,
              'thumbnail': 'https://www.lottehotel.com/content/dam/lotte-hotel/lotte/seoul/main/181023-1-2000-mai-LTSE.jpg.thumb.768.768.jpg'
              }]}
        )
        self.assertEqual(response.status_code, 200)

    def test_HotelDetailView_get_success(self):
        client = Client()
        response = self.client.get('/accommodations/hotels/1')
        self.assertEqual(response.json(),
            {
            "hotel_detail": {
                "id": 1,
                "name": "Lotte Hotel",
                "thumbnail_url": "https://www.lottehotel.com/content/dam/lotte-hotel/lotte/seoul/main/181023-1-2000-mai-LTSE.jpg.thumb.768.768.jpg",
                "description": "Ocean View",
                "basic_price": "333000.00",
                "checkin_time": "14:00:00",
                "checkout_time": "12:00:00",
                "city_id": 1,
                "location": "Somewhere only we know",
                "star": 5
            },
            "hotel_images": [
                'this_is_an_image.jpg'
            ],
            "hotel_conveniences": [
                {
                    "id": 1,
                    "name": "something good",
                    "icon_url": "icon.jpg"
                }
            ]}
        )
        self.assertEqual(response.status_code, 200)