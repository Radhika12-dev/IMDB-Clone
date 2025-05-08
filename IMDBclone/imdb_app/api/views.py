from imdb_app.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serialzers import *
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from .pagination import *

#Filtering the reviews based on the username of the reviewer by sending the username in the url
class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        user = self.kwargs['username']
        #As reviewer is a foreign key to the user model, we can filter the reviews based on the username of the reviewer
        return Review.objects.filter(reviewer__username=user)
    
#Filtering the reviews based on thequery parameters. http://127.0.0.1:8000/watch/reviews_query/?username=Radhika returns all the reviews of the user Radhika
class UserReviewQuery(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.request.query_params.get('username', None) 
        if username:
            queryset = Review.objects.filter(reviewer__username=username)
        return queryset
         
class WatchListAV(ListAPIView):
    # This will allow only the admin users to create a movie and other users can only view it.
    queryset = WatchList.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AdminOrReadOnly]  # Allow only admin users to create a movie

    #custom pagination class
    pagination_class = WatchListCursorPagination  # Use the custom pagination class
    
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
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
    permission_classes = [AdminOrReadOnly]
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
    permission_classes = [AdminOrReadOnly]
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
    

#http://127.0.0.1:8000/watch/stream/8/review/?reviewer__username=Radhika ... will give the list of all the reviews of the movie Radhika reviwed.
# this is the way we will use DjangoFilterBackend for generic views only and pass the query parameters on which we want to filter the data.
#These filter will find the exact match.
class ReviewList(generics.ListAPIView):
    
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]  # Enable throttling
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewer__username', 'active']  # Filter reviews by username and active fields
  
    #This will give the list of all the reviews of the particular movie = movie_id
    def get_queryset(self):
        pk = self.kwargs['movie_id']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]  # Allow only the user who created the review to edit or delete it. Other users can only view the review.

    # This throttle will limit the number of requests for this view only
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  # Enable throttling
    

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    # This will allow only the user who created the review to edit or delete it. Other users can only view the review.
    permission_class = [ReviewUserOrReadOnly]

    # This throttle will limit the number of requests for this view only. But the limit defined in settings.py will be applied to all the views i.e. total requests altogether to the all the apis will be limited to 1/day for anonymous users and 3/day for authenticated users.
    throttle_classes = [ReviewCreateThrottle]  # Enable custom throttling

    def get_queryset(self):
        return Review.objects.all()
       

    # This will create a review for the particular movie = movie_id
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a review.")
        
        movie_id = self.kwargs['movie_id']
        movie = WatchList.objects.get(pk=movie_id)

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

#filters.SearchFilter is used to search the data based on query parameters. 
#This filter will find the partial match.
# For example, if we search for 'net', it will return all the movies that have 'net' in their title or platform name.
# http://127.0.0.1:8000/watch/list2/?search=n ... is the url to search for the movies that have 'n' in their title or platform name.
class WatchListSearch(generics.ListAPIView):
    queryset = WatchList.objects.all()  # Correctly define the queryset
    serializer_class = MovieSerializer  # Reference the serializer class
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']  # Filter movies by title and platform name

# This will allow us to order the movies based on the title and platform name.

class WatchListOrdering(generics.ListAPIView):
    queryset = WatchList.objects.all()  # Correctly define the queryset
    serializer_class = MovieSerializer  # Reference the serializer class
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']