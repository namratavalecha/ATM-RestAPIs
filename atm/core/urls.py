from django.urls import path, re_path
from django.conf.urls import include
from .views import user_creation_form, create_atm, home, atm_validate, validate_view, transaction, api_deposit, deposit, signup, entry_view, withdraw, api_withdraw



app_name = 'core'

urlpatterns = [
    path('', entry_view, name="entry_view"),
    path('signup/', signup, name="signup"),
    path('home/', home, name="home"),
    path('create_user/', user_creation_form, name="create_user"),
    re_path(r'^generate_atm/(?P<id>\d+)/$', create_atm, name="generate_atm"),
    path('validate/', validate_view, name="validate"),
    path('transaction/', transaction, name="transaction"),
    path('atm_validate/', atm_validate, name="atm_validate"),
    path('api_deposit/', api_deposit, name="api_deposit"),
    path('deposit/', deposit, name="deposit"),
    path('withdraw/', withdraw, name="withdraw"),
    path('api_withdraw/', api_withdraw, name="api_withdraw"),
	]