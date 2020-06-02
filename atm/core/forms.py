from django import forms
from .models import Profile

class ProfileCreationForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['id','first_name', 'last_name', 'email', 'dob', 'address', 'bank', 'branch_name']