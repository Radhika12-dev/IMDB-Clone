from django.urls import path
from .views import registration_view, logout_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #This (obtain_auth_token) will generate a new token for authenticated users on passing username and password.
    path('login/', obtain_auth_token, name='api_login'),
    path('register/', registration_view, name='api_register'),
    path('logout/', logout_view, name='api_logout'), 
   
]