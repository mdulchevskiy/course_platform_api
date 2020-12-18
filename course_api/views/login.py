from django.db.models import Q
from rest_framework import (permissions,
                            status, )
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from course_api.models import PlatformUser
from course_api.serializers import UserSerializer


class LoginView(APIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        """Return information about authorized user."""
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    def post(self, request):
        """User authorization. Return user token if authorization was successful."""
        serializer = self.serializer_class(data=request.data)
        username = request.data.pop('username', None)
        errors = {} if username else {'username': ['This field is required.']}

        if serializer.is_valid() and username:
            password = serializer.validated_data.get('password')
            user = PlatformUser.objects.filter(Q(username=username) & Q(password=password)).first()
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            errors.update({'error': ["User with that username and password wasn't found."]})

        errors.update(serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
