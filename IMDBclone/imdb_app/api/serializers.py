from rest_framework import serializers

#Serializers define the API representation.

class MovieSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    active = serializers.BooleanField(default=True)

    
    