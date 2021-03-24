from django.db import models

# Create your models here.
class User(models.Model):
    name                = models.CharField(max_length=500)
    email               = models.EmailField(max_length=250)
    password            = models.CharField(max_length=250, null=True)
    location_is_agreed  = models.BooleanField()
    promotion_is_agreed = models.BooleanField()
    social_id           = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'users'
