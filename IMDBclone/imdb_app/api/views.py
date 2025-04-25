from imdb_app.models import Movie
from .serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

#In REST framework, we have to use @api_view decorator to define the function based views
@api_view(['GET'])
def movie_list(request):
    movie = Movie.objects.all()
    #when we have multiple objects we need to define many=True in serializer.
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data)  
@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data) 
