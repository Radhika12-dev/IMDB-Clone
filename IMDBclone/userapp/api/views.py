from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from .serializers import ResgistrationSerializer

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
        else:
            data = serializer.errors
        return Response(data)

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