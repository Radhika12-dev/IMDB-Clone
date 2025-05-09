from django.contrib.auth.models import User
from rest_framework import serializers

class ResgistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style ={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    #We are overriding the save method to create a user and set the password because existing User model does not have a password2 field
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        
        account = User(email = self.validated_data['email'],
                        username = self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account