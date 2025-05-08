from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from .serializers import ResgistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = ResgistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['username'] = account.username
            data['email'] = account.email
            #This will get the token from the signal created in signals.py which was executed when the user was created.
            token = Token.objects.create(user=account)
            data['token'] = token.key
            
        # This will create a JWT token(both access and refresh) for the user and send it back to the user.
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #     'access': str(refresh.access_token),
            #     'refresh': str(refresh),
            # }
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def logout_view(request):
    # Deletes the user's token when they log out. 
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response(status=204)
        except (AttributeError, Token.DoesNotExist):
            return Response(status=400)

#When user logs in, a token is created for the user and it is sent back to the user.