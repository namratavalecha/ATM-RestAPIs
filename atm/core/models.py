from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
User = settings.AUTH_USER_MODEL


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=False)
	last_name = models.CharField(max_length=100, blank=True)
	email = models.EmailField(max_length=150)
	dob = models.DateField()
	address = models.CharField(max_length = 200)
	bank = models.CharField(max_length = 50)
	branch_name = models.CharField(max_length = 50)
	amount = models.PositiveIntegerField(default=5000)
	atm_card_number = models.CharField(max_length = 8, unique = True, null=True, blank=True)
	atm_card_pin = models.CharField(max_length = 4, null=True, blank=True)


	def __str__(self):
		return self.first_name

	def return_id(self):
		return self.id


class Atm(models.Model):
	bank = models.CharField(max_length = 50)
	branch_name = models.CharField(max_length = 50)
	notes_2000 = models.PositiveIntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
	notes_500 = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(250)])
	notes_200 = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
	notes_100 = models.PositiveIntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])



