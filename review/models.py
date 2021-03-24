from django.db import models

from hotel.models import Hotel
from user.models  import User

# Create your models here.
class Review(models.Model):
    hotel      = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    rating     = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    title      = models.CharField(max_length=500)
    content    = models.TextField()

    class Meta():
        db_table = 'reviews'