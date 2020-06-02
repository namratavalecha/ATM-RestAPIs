from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		fields = ['id' ,'first_name', 'last_name', 'email', 'dob', 'address', 'bank', 'branch_name']