from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'regions'


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name   = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'cities'


class Hotel(models.Model):
    name          = models.CharField(max_length=45)
    thumbnail_url = models.URLField(max_length=200, blank=True)
    description   = models.TextField()
    basic_price   = models.DecimalField(max_digits=10, decimal_places=2)
    checkin_time  = models.TimeField(auto_now=False)
    checkout_time = models.TimeField(auto_now=False)
    city          = models.ForeignKey(City, on_delete=models.CASCADE)
    location      = models.CharField(max_length=500)
    star          = models.IntegerField(default = 5)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'hotels' 


class Option(models.Model):
    name  = models.CharField(max_length=45)
    hotel = models.ManyToManyField(Hotel, through = 'HotelOption')

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'options'


class HotelOption(models.Model):
    hotel            = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    option           = models.ForeignKey(Option, on_delete=models.CASCADE)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta():
        db_table = 'hotel_options'


class HotelImage(models.Model):
    hotel     = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200, blank=True)

    class Meta():
        db_table = 'hotel_images'


class Convenience(models.Model):
    name     = models.CharField(max_length=45)
    icon_url = models.URLField(max_length=200, blank=True)
    hotel    = models.ManyToManyField(Hotel, through = 'HotelConvenience')

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'conveniences'


class HotelConvenience(models.Model):
    hotel       = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    convenience = models.ForeignKey(Convenience, on_delete=models.CASCADE)

    class Meta():
        db_table = 'hotel_conveniences'


class Theme(models.Model):
    name  = models.CharField(max_length=45)
    hotel = models.ManyToManyField(Hotel, through = 'HotelTheme')

    def __str__(self):
        return self.name
    
    class Meta():
        db_table = 'themes'


class HotelTheme(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    class Meta():
        db_table = 'hotel_themes'
