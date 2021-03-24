from django.urls import path
from hotel_booking.views import HotelBookingView, WishListView

urlpatterns = [
    path('', HotelBookingView.as_view()),
    path('/wish', WishListView.as_view()),
    path('/wish/<int:hotel_id>', WishListView.as_view())
]
