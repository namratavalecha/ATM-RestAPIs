from django.urls import path, re_path
from django.conf.urls import include
from .views import user_creation_form, create_atm, home, validate_atm


app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('create_user/', user_creation_form, name="create_user"),
    re_path(r'^generate_atm/(?P<id>\d+)/$', create_atm, name="generate_atm"),
    path('validate_atm/', validate_atm, name="validate_atm"),
	]