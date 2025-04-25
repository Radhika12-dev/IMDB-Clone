from django.urls import path
from imdb_app.api.views import * 

urlpatterns = [
    path('list/', movie_list , name='movie_list'),
    path('detail/<int:movie_id>/', movie_detail, name='movie_detail'),
    
]