from django.utils.decorators import method_decorator
from rest_framework import (permissions,
                            status,
                            viewsets, )
from rest_framework.decorators import action
from rest_framework.response import Response
from course_api.models import (Course,
                               Lection, )
from course_api.serializers import LectionSerializer
from course_api.tools import access_to_course_validation_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description='Update selected lection.'))
class LectionViewSet(viewsets.ModelViewSet):
    serializer_class = LectionSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    @staticmethod
    def clear_lection_data(lection_data):
        for lection in lection_data:
            lection.pop('course')
        return lection_data

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.filter(id=course_id).first()
        return course_id, course

    def get_queryset(self):
        """Return lections from selected course."""
        course_id, _ = self.get_course()
        return Lection.objects.filter(course_id=course_id)

    @access_to_course_validation_decorator
    def list(self, request, *args, **kwargs):
        """List all lections from selected course."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(self.clear_lection_data(serializer.data))

    @access_to_course_validation_decorator
    def retrieve(self, request, *args, **kwargs):
        """Detail selected lection from selected course."""
        lection = self.get_object()
        serializer = self.get_serializer(lection)
        lection_data = serializer.data
        lection_data.pop('course')
        return Response(lection_data)

    @access_to_course_validation_decorator
    def create(self, request, *args, **kwargs):
        """
        Create lection and add it to selected course. POST method must include
        lection name field "topic". If expected field wasn't found, raise the error.
        """
        course_id, course = self.get_course()
        serializer = self.get_serializer(data=request.data)
        message = None
        if serializer.is_valid(raise_exception=True):
            received_fields = serializer.validated_data.keys()
            expected_field = 'topic'
            if expected_field in received_fields:
                serializer.save()
                lection = Lection.objects.get(id=serializer.data['id'])
                course.lections.add(lection)
                serializer = self.get_serializer(lection)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            message = {'error': f'The following arguments are expected: {expected_field}.'}
        errors = serializer.errors
        return Response(message or errors, status=status.HTTP_400_BAD_REQUEST)

    @access_to_course_validation_decorator
    def update(self, request, *args, **kwargs):
        """Update selected lection."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @access_to_course_validation_decorator
    def destroy(self, request, *args, **kwargs):
        """Delete selected lection."""
        return super().destroy(self, request, *args, **kwargs)

    @action(detail=False)
    def all(self, request, *args, **kwargs):
        """
        List all lections from all courses for authorized user depending on his role.
        """
        user = self.request.user
        role_user_id = getattr(user, user.role).id
        lection_role_dict = {
            'student': Lection.objects.filter(course__students__id=role_user_id),
            'teacher': Lection.objects.filter(course__teachers__id=role_user_id),
        }
        queryset = lection_role_dict[user.role]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
