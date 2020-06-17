from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from users.serializers import UserSerializers, AuthTokenSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """Create a new token for serializers"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage and authenticated user"""
    serializer_class = UserSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """retrieve and return authenticated user"""
        return self.request.user
