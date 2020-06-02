from django.shortcuts import render
from .forms import ProfileCreationForm
from django.shortcuts import render
import requests
from .models import Profile
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
# Create your views here.


def home(request):
	return render(request, 'home.html')

def user_creation_form(request):
	if request.method == 'POST':
		print(request.POST)
		profile_form = ProfileCreationForm(request.POST)
		if profile_form.is_valid():
			user_obj = profile_form.save()
			id = user_obj.return_id()
			r = requests.post('http://127.0.0.1:8000/generate_atm/{}/'.format(id))
			atm_card_number = r.json().get('atm_card_number')
			atm_card_pin = r.json().get('atm_card_pin')
			return render(request, 'atm.html', {'atm_card_number':atm_card_number, 'atm_card_pin':atm_card_pin})
	else:
		profile_form = ProfileCreationForm()
	return render(request, 'user_creation.html', {'profile_form':profile_form})



@api_view(['POST'])
def create_atm(request, id):
	print(request.POST)
	user_id = request.POST.get('id')
	user_obj = Profile.objects.filter(id=id)
	if user_obj.exists():
		atm_card = user_obj[0].atm_card_number
		if atm_card:
			atm_pin = user_obj[0].atm_card_pin
			return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'ATM card already exists', 'atm_card_number':atm_card, 'atm_card_pin': atm_pin})
		else:
			atm_card_number = int(get_random_string(8, '123456789'))
			atm_pin = int(get_random_string(4, '123456789'))
			Profile.objects.filter(id=id).update(atm_card_number=atm_card_number, atm_card_pin= atm_pin)
			return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'ATM card created', 'atm_card_number':atm_card_number, 'atm_card_pin': atm_pin})
	else:
		return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'user does not exist'})


@api_view(['POST'])
def validate_atm(request):
	print(request.POST)
	atm_number = request.POST.get('atm_number')
	atm_pin = request.POST.get('atm_pin')
	user_obj = Profile.objects.filter(atm_card_number=atm_number)
	if user_obj.exists():
		atm_card_pin = user_obj[0].atm_card_pin
		if (atm_card_pin == atm_pin):
			return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'Validation Successful'})
		else:
			return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'Wrong Pin'})
	else:
		return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Invalid ATM Card Number'})