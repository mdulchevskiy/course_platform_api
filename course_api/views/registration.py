from rest_framework import (permissions,
                            status, )
from rest_framework.response import Response
from rest_framework.views import APIView
from course_api.serializers import UserSerializer


class RegistrationView(APIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        """
        User registration. POST method must include all field in user model.
        If expected fields weren't found, raise the error with expected fields.
        """
        serializer = self.serializer_class(data=request.data)
        message = None
        if serializer.is_valid(raise_exception=True):
            received_fields = set(serializer.validated_data.keys())
            expected_fields = set(serializer.fields.keys())
            expected_fields.remove('id')
            if received_fields == expected_fields:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            expected_arguments = expected_fields.difference(received_fields)
            message = {'error': f"The following arguments are expected: {', '.join(expected_arguments)}."}
        errors = serializer.errors
        return Response(message or errors, status=status.HTTP_400_BAD_REQUEST)
