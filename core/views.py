from django.shortcuts import render, redirect
from .forms import ProfileCreationForm
from django.shortcuts import render
import requests
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Atm
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
# Create your views here.

try:
	atm = Atm.objects.get_or_create(id = 1, bank="Bank", branch_name="abc")
except Exception as e:
	print(e)


def entry_view(request):
	return render(request, 'entry.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



def home(request):
	return render(request, 'home.html')

def user_creation_form(request):
	if request.method == 'POST':
		profile_form = ProfileCreationForm(request.POST)
		user = User.objects.filter(id = request.user.id)
		if not user.exists():
			return redirect('core:signup')
		else:
			temp = Profile.objects.filter(user = user[0])
			if not temp.exists():
				if profile_form.is_valid():
					user_obj = profile_form.save(commit=False)
					user_obj.user = user[0]
					user_obj.save()
					id = user_obj.return_id()
			else:
				id = temp[0].return_id()
			r = requests.post('http://127.0.0.1:8000/generate_atm/{}/'.format(id))
			message = r.json().get('message')
			atm_card_number = r.json().get('atm_card_number')
			atm_card_pin = r.json().get('atm_card_pin')
			return render(request, 'atm.html', {'message': message, 'atm_card_number':atm_card_number, 'atm_card_pin':atm_card_pin})

	else:
		profile_form = ProfileCreationForm()
	return render(request, 'user_creation.html', {'profile_form':profile_form})



@api_view(['POST'])
def create_atm(request, id):
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



def validate_view(request):
	return render(request, 'atm_validation.html')


@api_view(['POST'])
def atm_validate(request):
	atm_number = request.POST.get('atm_number')
	atm_pin = request.POST.get('atm_pin')
	user_obj = Profile.objects.filter(atm_card_number=atm_number)
	if user_obj.exists():
		atm_card_pin = user_obj[0].atm_card_pin
		if (atm_card_pin == atm_pin):
			return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'Validation Successful'})
		else:
			return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Wrong Pin'})
	else:
		return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Invalid ATM Card Number'})


def transaction(request):
	return render(request, 'transaction.html')



def deposit(request):
	return render(request, 'deposit.html')


@api_view(['POST'])
def api_deposit(request):
	username = request.POST.get('username')
	user_obj = User.objects.filter(username = username)
	if user_obj.exists():
		no_2000 = int(request.POST.get('no_2000')) if 'no_2000' in request.POST else 0
		no_500 = int(request.POST.get('no_500')) if 'no_500' in request.POST else 0
		no_200 = int(request.POST.get('no_200')) if 'no_200' in request.POST else 0
		no_100 = int(request.POST.get('no_100')) if 'no_100' in request.POST else 0
		total = 2000*no_2000 + 500*no_500 + 200*no_200 + 100*no_100
		profile = Profile.objects.filter(user = user_obj[0])
		if profile.exists():
			current_amount = profile[0].amount
			new_amount = total+current_amount
			Profile.objects.filter(user = user_obj[0]).update(amount = new_amount)

			obj = Atm.objects.filter(id=1)
			ini_2000 = obj[0].notes_2000
			ini_500 = obj[0].notes_500
			ini_200 = obj[0].notes_200
			ini_100 = obj[0].notes_100

			Atm.objects.filter(id=1).update(
				notes_2000 = ini_2000 + no_2000,
				notes_500 = ini_500 + no_500,
				notes_200 = ini_200 + no_200,
				notes_100 = ini_100 + no_100)
			return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'Money Deposited successfully', 'current_balance': new_amount})
		else:
			return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Issue an ATM card first'})
	else:
		return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'You are not authorized'})



def withdraw(request):
	return render(request, 'withdraw.html')



@api_view(['POST'])
def api_withdraw(request):
	username = request.POST.get('username')
	user_obj = User.objects.filter(username = username)
	if user_obj.exists():
		profile = Profile.objects.filter(user = user_obj[0])
		if profile.exists():
			amount = int(request.POST.get('amount')) if 'amount' in request.POST else 0
			if (amount > 20000):
				return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Withdraw limit is 20000'})
			if(amount % 100 != 0 or amount==0): 
				return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Please enter the amount in multiples of 100'})
			current_amount = profile[0].amount
			if(current_amount - amount <= 0):
				return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Not enough money in your account'})
			obj = Atm.objects.filter(id=1)
			existing_denom = {}
			existing_denom[2000] = obj[0].notes_2000
			existing_denom[500] = obj[0].notes_500
			existing_denom[200] = obj[0].notes_200
			existing_denom[100] = obj[0].notes_100
			total = 0
			for k in existing_denom.keys():
				total += k*existing_denom[k]
			if(amount > total):
				return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Not enough money in the machine'})
			transaction = {}
			amt = amount
			denom_keys = sorted(existing_denom.keys(), reverse=True) 
			for k in denom_keys:
				if (existing_denom[k] - (amt//k) >= 0):
					transaction[k] = amt//k
				else:
					transaction[k] = existing_denom[k]
				amt -= k*transaction[k]
			if amt != 0 :
				return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Not enough money in the machine'})
			Atm.objects.filter(id=1).update(
				notes_2000 = existing_denom[2000]-transaction[2000],
				notes_500 = existing_denom[500]-transaction[500],
				notes_200 = existing_denom[200]-transaction[200],
				notes_100 = existing_denom[100]-transaction[100],
				)
			new_amount = current_amount - amount
			Profile.objects.filter(user = user_obj[0]).update(amount = new_amount)
			return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'Money Withdrawn successfully', 'current_balance': new_amount, 'transaction': transaction})
		else:
			return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Issue an ATM card first'})
	else:
		return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'You are not authorized'})

