from django.urls import path
from hotel.views import HotelListView, HotelDetailView

urlpatterns = [
    path('/hotels', HotelListView.as_view()),
    path('/hotels/<int:hotel_id>', HotelDetailView.as_view()),
]
