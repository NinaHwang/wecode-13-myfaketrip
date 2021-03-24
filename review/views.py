import json
import decimal

from django.http      import JsonResponse
from django.views     import View

from review.models import Review
from hotel.models import Hotel
from user.models import User

# Create your views here.

class HotelReviewView(View):

     @utils.signin_decorator
    def post(self, request, hotel_id):
        json.loads(request.body)
        user_id = request.user.id

        Review.objects.create(
            rating = data['rating'],
            title = data['title'],
            content = data['content'],
            hotel_id = Hotel.objects.get(id=hotel_id),
            user_id = User.objects.get(id=user_id)
        )

        review_list = [review for review in Review.objects.filter(hotel_id = hotel_id).values()][::-1]

        returning_list = [
            {
                'id' : review['id'],
                'user' : review['user_id'],
                'rating' : review['rating'],
                'created_at' : review['created_at'].strftime("%Y-%m-%dT%H:%M:%S"),
                'title' : review['title'],
                'content' : review['content']
            }
            for review in review_list
        ]


        return JsonResponse(
            {'review_list':returning_list},
            status=201
        )



    def get(self, request, hotel_id):
        hotel_id = hotel_id
        review_list = [review for review in Review.objects.filter(hotel_id = hotel_id).values()][::-1]

        returning_list = [
            {
                'id' : review['id'],
                'user' : review['user_id'],
                'rating' : review['rating'],
                'created_at' : review['created_at'].strftime("%Y-%m-%dT%H:%M:%S"),
                'title' : review['title'],
                'content' : review['content']
            }
            for review in review_list
        ]


        return JsonResponse(
            {'review_list':returning_list},
            status=200
        )

    @utils.signin_decorator
    def patch(self, request, review_id):
        json.loads(request.body)

        target_review = Review.objects.get(id=review_id)
        user_id = request.user.id

        if user_id != Review.objects.get(id=review_id).user_id :
            return JsonResponse({'message : NO_PERMISSION',status=403})

        review_field_list = Review._meta.get_fields()

        for field in review_field_list:
            if field in data:
                target_review.update(**{field:data[field]})

        review_list = [review for review in Review.objects.filter(hotel_id = hotel_id).values()][::-1]

        returning_list = [
            {
                'id' : review['id'],
                'user' : review['user_id'],
                'rating' : review['rating'],
                'created_at' : review['created_at'].strftime("%Y-%m-%dT%H:%M:%S"),
                'title' : review['title'],
                'content' : review['content']
            }
            for review in review_list
        ]

        return JsonResponse(
            {'review_list':returning_list},
            status=201
        )

    @utils.signin_decorator
    def delete(self, request, review_id):
        target_review = Review.objects.get(id=review_id)
        user_id = request.user.id

        if user_id != Review.objects.get(id=review_id).user_id :
            return JsonResponse({'message : NO_PERMISSION',status=403})

        target_review.delete()

        return JsonResponse(
            {'meesage':'DELETED'},
            status=200
        )

