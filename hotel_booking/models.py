from django.db import models
from user.models import User
from hotel.models import HotelOption, Hotel

# Create your models here.
class HotelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_option = models.ForeignKey(HotelOption, on_delete=models.CASCADE)

    class Meta():
        db_table = 'hotel_bookings'

class BookingInfo(models.Model):
    hotel_booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE)
    name          = models.CharField(max_length=50)
    sex           = models.CharField(max_length=50)
    birth         = models.DateField(auto_now=False, auto_now_add=False)
    checkin_date  = models.DateField(auto_now=False, auto_now_add=False)
    checkout_date = models.DateField(auto_now=False, auto_now_add=False)
    arrival_time  = models.TimeField(auto_now=False, auto_now_add=False)
    mobile        = models.CharField(max_length=100)
    total_people  = models.IntegerField()

    class Meta():
        db_table = 'booking_infos'

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'wishlists'
