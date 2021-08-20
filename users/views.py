from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from users import serializers, models
from rest_framework.authentication import TokenAuthentication
from users import permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login


class HealthApiView(APIView):
    """Check whether all api are working or not"""
    def get(self, request):
        return Response(True)


class UserRegisterViewSet(viewsets.ModelViewSet):
    """Handle creating and updating users"""
    serializer_class = serializers.UserRegisterSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
    def post(self, request):
        """Get token for a user"""
        user = models.User.objects.get(email=request.data['username'])
        if not user:
            return Response({"status": False, "message": "Sorry, we can't find an account with this email address"})

        valid_user = authenticate(request, email=request.data['username'], password=request.data['password'])
        if user.is_active == False:
            return Response({"message": "Email not verified Please check your email", "status": False})
        if valid_user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email
            })            
        else: 
            return Response({"status": False, "message": "OOPS, Invalid credentials"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        

class UserProfileViewSet(viewsets.ModelViewSet):
    """Get user profile from database"""
    serializer_class = serializers.UserRegisterSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    
    


class UserLogout(APIView):
    """Delete token from database"""
    def get(self, request):
        """log out user"""
        try: 
            request.user.auth_token.delete()
        except:
            pass
        return Response(status=status.HTTP_200_OK)



