from imdb_app.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serialzers import *
from rest_framework.exceptions import ValidationError
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly
class WatchListAV(APIView):
    def get(self, reques):
        movie = WatchList.objects.all()
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class WatchDetailAV(APIView):
    def get(self, request, movie_id):
        try:
            movie = WatchList.objects.get(id=movie_id)
        except WatchList.DoesNotExist:
            return Response(status=404)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, movie_id):
        movie = WatchList.objects.get(id=movie_id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, movie_id):
        movie = WatchList.objects.get(id=movie_id)
        movie.delete()
        return Response(status=204)

class StreamPlatformAV(APIView):
    def get(self, request):
        platforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(platforms, many=True, context={'request': request}
                                                 )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class StreamDetailAV(APIView):
    def get(self, request, platform_id):
        try:
            platform = StreamingPlatform.objects.get(id=platform_id)
        except StreamingPlatform.DoesNotExist:
            return Response(status=404)
        serializer = StreamingPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, platform_id):
        platform = StreamingPlatform.objects.get(id=platform_id)
        serializer = StreamingPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, platform_id):
        platform = StreamingPlatform.objects.get(id=platform_id)
        platform.delete()
        return Response(status=204)

# here we are using mixins to create a generic view for the review list and detail
# we can't change the variable names like queryset and serializer_class in the class based views
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
    
class ReviewList(generics.ListAPIView):
    
    serializer_class = ReviewSerializer
    # Now only admin users can access the review list of a particular movie and other can view it
    permission_classes = [IsAuthenticated]


    #This will give the list of all the reviews of the particular movie = movie_id
    def get_queryset(self):
        pk = self.kwargs['movie_id']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    # This will allow only the user who created the review to edit or delete it. Other users can only view the review.
    permission_class = [ReviewUserOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()
       

    # This will create a review for the particular movie = movie_id
    def perform_create(self, serializer):
        pk = self.kwargs['movie_id']
        movie = WatchList.objects.get(pk=pk)

        #Only one review can be created by one user for one movie
        reviewer = self.request.user
        reviewer_query  = Review.objects.filter(reviewer=reviewer, watchlist=movie)
        if reviewer_query.exists():
            raise serializers.ValidationError("You have already reviewed this movie")
        
        if movie.total_ratings == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
        movie.total_ratings += 1 
        movie.save()
        serializer.save(watchlist=movie, reviewer=reviewer)
    # We have multiple functions that can be overrided to customize the behavior of our API views, like perform_create, perform_update, perform_destroy, etc.

