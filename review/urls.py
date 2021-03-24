from django.urls import path
from review.views import HotelReviewView

urlpatterns = [
    path('/<int:hotel_id>', HotelReviewView.as_view())
]
