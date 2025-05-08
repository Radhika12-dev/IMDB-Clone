from rest_framework import serializers
from imdb_app.models import *

class ReviewSerializer(serializers.ModelSerializer):
    # Nested serializer to show the movie title in the review
    reviewer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        # fields = ['rating', 'description', 'watchlist']

class MovieSerializer(serializers.ModelSerializer):
    days_since_added = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name', read_only=True)
    # This will show the reviews related to the movie in the list
    class Meta:
        model = WatchList
        fields = '__all__'
    def get_days_since_added(self, obj):
        return (now() - obj.created_at).days
    
class StreamingPlatformSerializer(serializers.ModelSerializer):
    # By default, the related_name is 'watchlist' in model for reverse relation
    # Creating a custom field to show all the movies that belong to particular streaming platform
    # watchlist = MovieSerializer(many=True, read_only=True)
    watchlist = serializers.StringRelatedField(many=True, read_only=True)
    #This will show the string representation of the movie object in the list

   
    class Meta:
        model = StreamingPlatform
        fields = '__all__'