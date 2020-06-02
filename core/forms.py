from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileCreationForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'email', 'dob', 'address', 'bank', 'branch_name']

