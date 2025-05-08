from django.urls import path
from imdb_app.api.views import * 

urlpatterns = [
    path('list/', WatchListAV.as_view() , name='movie_list'),
    path('detail/<int:movie_id>/', WatchDetailAV.as_view(), name='movie_detail'),
    path('stream/', StreamPlatformAV.as_view(), name='stream_platform'),
    path('stream/<int:platform_id>/', StreamDetailAV.as_view(), name='stream_detail'),

    # These urls giving reviews of all the watchlist items which is incorrect
    # path('review/', ReviewList.as_view(), name='review_list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),

    path('stream/<int:movie_id>/review/', ReviewList.as_view(), name='review_list'),
    path('stream/<int:movie_id>/review-create/', ReviewCreate.as_view(), name='review_create'),
    path('stream/review/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),
    path('reviews/<str:username>/', UserReview.as_view(), name='user_review_list'),
    path('reviews_query/',UserReviewQuery.as_view(), name='user_review_query'),
    path('list2/', WatchListSearch.as_view() , name='movie_list2'),
    path('list3/', WatchListOrdering.as_view() , name='movie_list3'),
    
]   