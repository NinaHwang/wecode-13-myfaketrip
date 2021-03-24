import json
import utils

from django.http import JsonResponse
from django.views import View

from hotel_booking.models import HotelBooking, BookingInfo, WishList
from hotel.models import Hotel, Option, HotelOption
from user.models import User


# Create your views here.

class HotelBookingView(View):
    @utils.signin_decorator
    def post(self, request):
        try:
            data            = json.loads(request.body)
            user_id         = request.user.id
            hotel_id        = data['hotel']
            hotel_option_id = data['option']
            target_hotel    = [hotel_option for hotel_option in HotelOption.objects.filter(hotel = hotel_id, option_id = hotel_option_id).values()][0]
            hotel_price     = [hotel['basic_price'] for hotel in Hotel.objects.filter(id = hotel_id).values()]
            option_price    = target_hotel['additional_price']

            total_price = int(hotel_price[0]) + int(option_price)

            booking_data, flag = HotelBooking.objects.get_or_create(
                                    user_id         = user_id,
                                    hotel_option_id = target_hotel['id'],
                                )

            BookingInfo.objects.create(
                hotel_booking_id = booking_data.id,
                name             = data['name'],
                sex              = data['sex'],
                birth            = data['birth'],
                checkin_date     = data['checkin_date'],
                checkout_date    = data['checkout_date'],
                arrival_time     = data['arrival_time'],
                mobile           = data['mobile'],
                total_people     = data['total_people']
            )

            return JsonResponse(
                {'message': 'BOOKING SUCCESS'},
                status=201
            )
    
        except KeyError:
            return JsonResponse(
                {'message': 'KEY_ERROR'},
                status=400
            )

    @utils.signin_decorator
    def get(self, request):
        try:
            user_id = request.user.id
            
            booking_hotels = HotelBooking.objects.select_related('hotel_option__hotel').prefetch_related('bookinginfo_set').filter(user_id=user_id)
            
            booking_list = [
                {
                    'hotel_thumbnail' : booking.hotel_option.hotel.thumbnail_url,
                    'hotel_name' : booking.hotel_option.hotel.name,
                    'checkin_date':booking.bookinginfo_set.all()[0].checkin_date
                } for booking in booking_hotels
            ]

            return JsonResponse(
                {'booking_list':booking_list},
                status=200
            )
        
        except KeyError:
            return JsonResponse(
                {'message': 'KEY_ERROR'},
                status=400
            )


class WishListView(View):
    @utils.signin_decorator
    def post(self, request, hotel_id):
        wished_hotel = hotel_id
        user_id = request.user.id

        WishList.objects.create(
            user_id = user_id,
            hotel_id = wished_hotel
        )

        return JsonResponse(
            {'message': 'ADDED_TO_WISHLIST'},
            status=201
        )

    @utils.signin_decorator
    def get(self, request):
        user_id = request.user.id
        wished_hotels = WishList.objects.select_related('hotel').filter(user_id = user_id)
        
        wish_list = [
            {
                'hotel_thumbnail' : hotel.hotel.thumbnail_url,
                'hotel_name' : hotel.hotel.name,
                'hotel_price' : hotel.hotel.basic_price
            } for hotel in wished_hotels
        ]

        return JsonResponse(
                {'wishlist':wish_list},
                status=200
            )