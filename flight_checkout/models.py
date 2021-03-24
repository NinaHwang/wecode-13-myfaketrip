from django.db      import models

class BookingInfo(models.Model):
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)
    start_flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE, related_name='start_flight')
    end_flight   = models.ForeignKey('flight.Flight', on_delete=models.CASCADE, related_name='end_flight')
    start_date   = models.DateField()
    end_date     = models.DateField()
    total_people = models.IntegerField()
   
    class Meta:
        db_table = 'flight_booking_info'