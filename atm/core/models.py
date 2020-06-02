from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    dob = models.DateField()
    address = models.CharField(max_length = 200)
    bank = models.CharField(max_length = 50)
    branch_name = models.CharField(max_length = 50)
    amount = models.IntegerField(default=2000)
    atm_card_number = models.CharField(max_length = 8, unique = True)
    atm_card_pin = models.CharField(max_length = 4)

    def __str__(self):
        return self.user.username