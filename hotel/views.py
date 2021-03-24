import json
import decimal

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Max

from hotel.models     import Region, City, Hotel, Option, HotelOption, HotelImage, Convenience, HotelConvenience, Theme, HotelTheme
# Create your views here.

class HotelListView(View):

    def get(self, request):
        try:
        # 변수
            if not request.GET._mutable:
                request.GET._mutable = True

            filter_conditions = dict(request.GET)
            limit             = 10

            if filter_conditions.get('offset'):
                offset = filter_conditions['offset'][0]
                del filter_conditions['offset']
            else:
                offset = 0

            if filter_conditions.get('order_by'):
                order_by = filter_conditions.get('order_by')[0]
                del filter_conditions['order_by']
            else:
                order_by = None

        # 필터
            # 등급 필터
            if filter_conditions.get('star'):
                filter_conditions["star__in"] = filter_conditions.pop('star')

            # 가격 필터
            if filter_conditions.get('min_price'):
                minimum = int(filter_conditions.get('min_price'))
            else:
                minimum = 0
            if filter_conditions.get('max_price'):
                maximum = int(filter_conditions.get('max_price'))
            else:
                maximum = int(Hotel.objects.all().aggregate(Max('basic_price'))['basic_price__max'])
            filter_conditions["basic_price__range"] =  (minimum, maximum)

             # 서비스 필터
            if filter_conditions.get('convenience'):
                hotels = list(set([
                    hotel['hotel_id'] 
                    for hotel 
                    in HotelConvenience.objects.filter(
                        convenience_id = filter_conditions.get('convenience')[0]
                        ).values()
                        ]))
                del filter_conditions['convenience']
                filter_conditions["id__in"] = hotels


            # 테마 필터
            if filter_conditions.get('theme'):
                hotels = [
                    hotel['hotel_id'] 
                    for hotel 
                    in HotelTheme.objects.filter(theme_id = filter_conditions.get('theme')[0]
                    ).values()
                ]
                del filter_conditions['theme']
                filter_conditions["id__in"] = hotels

            # 지역 필터
            if filter_conditions.get('region'):
                cities = City.objects.filter(region_id = filter_conditions.get('region')[0])
                filter_conditions['city__in'] = cities
                del filter_conditions['region']

            if (filter_conditions.get('city_id') == None) and (filter_conditions.get('city__in') == None):
                filter_conditions['city_id'] = 1
            

            if order_by != None:
                sorting = {
                'star': '-star',
                'price_high':'-basic_price',
                'price_low' : 'basic_price'
                }
                filtered_hotel = Hotel.objects.filter(**filter_conditions).order_by(sorting[order_by]).values()
    
            else:
                filtered_hotel = Hotel.objects.filter(**filter_conditions).values()

            total_hotels = len(filtered_hotel)

            if offset > len(filtered_hotel):
                return JsonResponse({
                    "message": "Offset out of range"
                })
            
            hotel_list = [hotel for hotel in filtered_hotel][offset:offset+limit]

            returning_list = []

            for hotel in hotel_list:
                returning_dict = {}
                returning_dict['id']        = hotel['id']
                returning_dict['name']      = hotel['name']
                returning_dict['thumbnail'] = hotel['thumbnail_url']
                returning_dict['price']     = hotel['basic_price']
                returning_dict['star']      = hotel['star']
                returning_list.append(returning_dict)

        # 지역 필터 모달..........
            region_list = Region.objects.all().values()
            city_list = City.objects.all().values()

            return JsonResponse(
                {
                    "hotels":returning_list,
                    "total_hotels":total_hotels,
                    "region" :[region['name'] for region in region_list],
                    "city" : [city['name'] for city in city_list]
                },
                status=200
                )

        except ValueError:
            return JsonResponse(
                {
                    "message": "Given input is not valid"
                }
            )


class HotelDetailView(View):
    def get(self, request, hotel_id):
        hotel_detail       = Hotel.objects.filter(id = hotel_id).values()[0]
        hotel_images       = [image['image_url'] for image in HotelImage.objects.filter(hotel_id = hotel_id).values()]
        hotel_conveniences = [conv['convenience_id'] for conv in HotelConvenience.objects.filter(hotel_id = hotel_id).values()]
        


        hotel_conveniences_list = []
        for conv in hotel_conveniences:
            target_con = Convenience.objects.filter(id = conv).values()[0]
            hotel_conveniences_list.append(target_con)
        hotel_conveniences_list = [
            Convenience.objects.filter(id = conv).values()[0] for conv in hotel_conveniences
        ]

        hotel_add_prices = [option['additional_price'] for option in HotelOption.objects.filter(hotel_id=hotel_id).values()]

        return JsonResponse({
            'hotel_detail'      : hotel_detail,
            'hotel_images'      : hotel_images,
            'hotel_conveniences': hotel_conveniences_list,
            'hotel_add_prices'  : hotel_add_prices
            },
            status=200
        )
