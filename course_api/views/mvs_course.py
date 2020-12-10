from django.utils.decorators import method_decorator
from rest_framework import (permissions,
                            status,
                            viewsets, )
from rest_framework.decorators import action
from rest_framework.response import Response
from course_api.models import Course
from course_api.serializers import CourseSerializer
from drf_yasg.utils import swagger_auto_schema
from course_api.tools import openapi_ready


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description='Update selected course.'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description='Delete selected course.'))
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    @staticmethod
    def clear_data(course_data, option=None):
        if option:
            for lection in course_data['lections']:
                lection.pop('course')
        else:
            for course in course_data:
                course.pop('students')
                course.pop('lections')
        return course_data

    @openapi_ready(Course)
    def get_queryset(self):
        """Return courses available for authorized user."""
        user = self.request.user
        return getattr(user, user.role).courses

    def list(self, request, *args, **kwargs):
        """List courses available for authorized user."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(self.clear_data(serializer.data))

    def retrieve(self, request, *args, **kwargs):
        """Detail selected course."""
        course = self.get_object()
        serializer = self.get_serializer(course)
        return Response(self.clear_data(serializer.data, option=True))

    def create(self, request, *args, **kwargs):
        """
        Create course. POST method must include course name field "name".
        If expected field wasn't found, raise the error.
        """
        serializer = self.get_serializer(data=request.data)
        message = None
        if serializer.is_valid(raise_exception=True):
            received_fields = set(serializer.validated_data.keys())
            expected_field = 'name'
            if expected_field in received_fields:
                serializer.save()
                teacher = self.request.user.teacher
                course = Course.objects.get(id=serializer.data['id'])
                teacher.courses.add(course)
                return Response(status=status.HTTP_201_CREATED)
            message = {'error': f'The following arguments are expected: {expected_field}.'}
        errors = serializer.errors
        return Response(errors or message, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Update selected course."""
        instance = super().update(request, *args, **kwargs)
        self.clear_data(instance.data, option=True)
        return instance

    @action(detail=False)
    def all(self, request, *args, **kwargs):
        """List all courses in the system."""
        queryset = Course.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(self.clear_data(serializer.data))
