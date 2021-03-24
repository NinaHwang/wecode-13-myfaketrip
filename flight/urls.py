from django.urls  import path
from flight.views import FlightScheduleView

urlpatterns = [
    path('',FlightScheduleView.as_view())
]
