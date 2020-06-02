from django.urls import path, re_path
from django.conf.urls import include
from .views import user_creation_form


app_name = 'core'

urlpatterns = [
    path('create_user/', user_creation_form, name="create_user"),
	]