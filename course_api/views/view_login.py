from django.db.models import Q
from rest_framework import (permissions,
                            status, )
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from course_api.models import PlatformUser
from course_api.serializers import UserSerializer


class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        """Return information about authorized user."""
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    def post(self, request):
        """User authorization. Return user token if authorization was successful."""
        username = self.request.data.get("username")
        password = self.request.data.get("password")
        if not username or not password:
            data = {'error': 'Please provide both username and password.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user = PlatformUser.objects.filter(Q(username=username) & Q(password=password)).first()

        if not user:
            data = {'error': "User with that username and password wasn't found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
