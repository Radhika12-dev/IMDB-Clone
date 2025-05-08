from django.urls import path
from .views import registration_view, logout_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#These URLs are using token authentication
urlpatterns = [
    #This (obtain_auth_token) will generate a new token for authenticated users on passing username and password.
    path('login/', obtain_auth_token, name='api_login'),
    path('register/', registration_view, name='api_register'),
    path('logout/', logout_view, name='api_logout'), 

    #These new URLs are using JWT authentication
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]

