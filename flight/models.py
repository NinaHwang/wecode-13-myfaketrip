from django.db import models

class Airline(models.Model):
    name     = models.CharField(max_length=45)
    eng_name = models.CharField(max_length=45, default='')
    logo_url = models.URLField(max_length=1000, default='')

    class Meta:
        db_table = 'airlines'

class Airport(models.Model):
    name     = models.CharField(max_length=45)
    eng_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'airports'

class Flight(models.Model):
    airline        = models.ForeignKey(Airline, on_delete=models.CASCADE)
    flightid       = models.CharField(max_length=45)
    airport_depart = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name = 'depart')
    airport_arrive = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name = 'arrive')
    depart_time    = models.TimeField()
    arrive_time    = models.TimeField()
    start_date     = models.DateField()
    end_date       = models.DateField()
    remain_seats   = models.IntegerField(default=0)
    seat_class     = models.CharField(max_length=45)
    basic_price    = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)

    class Meta:
        db_table = 'flights'

class Weekday(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'weekdays'

class FlightWeekday(models.Model):
    flight  = models.ForeignKey(Flight, on_delete=models.CASCADE)
    date    = models.DateField()
    weekday = models.CharField(max_length=45)

    class Meta:
        db_table = 'flight_weekdays'