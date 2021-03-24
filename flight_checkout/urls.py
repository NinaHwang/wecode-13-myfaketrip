from django.urls           import path
from flight_checkout.views import FlightBookingView

urlpatterns = [
    path('', FlightBookingView.as_view())
]