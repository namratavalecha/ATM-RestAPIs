from django.shortcuts import render
from .forms import ProfileCreationForm
from django.shortcuts import render
import uuid
from .models import Profile
from rest_framework.decorators import api_view
# Create your views here.

def user_creation_form(request):
	if request.method == 'POST':
		form = ProfileCreationForm(request.POST)
		if form.is_valid():
			id = form.cleaned_data.get('id')
			form.save()
			
			return render('atm.html')

	else:
		form = ProfileCreationForm()
	return render(request, 'user_creation.html', {'form':form})


@api_view(['POST'])
def create_atm(request, id):
    print(request.POST)
    user_id = request.POST.get('id')
    user_obj = Profile.objects.filter(id=id)
    if note_obj.exists():
    	atm_card_number = user_obj[0].atm_card_number
    	atm_pin = user_obj[0].atm_pin
    	return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'ATM card already exists', 'atm_card_number':atm_card_number, 'atm_pin': atm_pin})
    else:
    	atm_card_number = uuid.uuid4().hex[:8]
    	atm_pin = uuid.uuid().hex[:4]
        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'ATM card created', 'atm_card_number':atm_card_number, 'atm_pin': atm_pin})
