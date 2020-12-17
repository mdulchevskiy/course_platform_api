from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import (permissions,
                            status,
                            viewsets, )
from rest_framework.decorators import action
from rest_framework.response import Response
from course_api.models import (Course,
                               Homework,
                               Lection,
                               Student, )
from course_api.serializers import HomeworkSerializer
from course_api.tools import (access_to_course_validation_decorator,
                              lection_existence_validation_decorator, )
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description='Update selected homework for selected lection.'))
class HomeworkViewSet(viewsets.ModelViewSet):
    serializer_class = HomeworkSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    @staticmethod
    def clear_homework_data(homework_data):
        for homework in homework_data:
            homework.pop('lection')
        return homework_data

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.filter(id=course_id).first()
        return course_id, course

    def get_lection(self):
        course_id, _ = self.get_course()
        lection_id = self.kwargs.get('lection_id')
        lection = Lection.objects.filter(Q(course_id=course_id) & Q(id=lection_id)).first()
        return lection_id, lection

    def get_queryset(self):
        """Return homeworks for selected lection."""
        lection_id, _ = self.get_lection()
        return Homework.objects.filter(lection_id=lection_id)

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def list(self, request, *args, **kwargs):
        """List all homeworks for selected lection."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(self.clear_homework_data(serializer.data))

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def retrieve(self, request, *args, **kwargs):
        """Detail selected homework for selected lection."""
        homework = self.get_object()
        serializer = self.get_serializer(homework)
        homework_data = serializer.data
        homework_data.pop('lection')
        return Response(homework_data)

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def create(self, request, *args, **kwargs):
        """
        Create homework, add it to selected lecture and add it to students from
        selected course. POST method must include homework task field "task".
        If expected field wasn't found, raise the error.
        """
        course_id, _ = self.get_course()
        lection_id, lection = self.get_lection()
        serializer = self.get_serializer(data=request.data)
        message = None
        if serializer.is_valid(raise_exception=True):
            received_fields = serializer.validated_data.keys()
            expected_field = 'task'
            if expected_field in received_fields:
                serializer.save()
                homework = Homework.objects.get(id=serializer.data['id'])
                students = Student.objects.filter(courses__id=course_id)
                with transaction.atomic():
                    lection.homeworks.add(homework)
                    homework.students.set(students)
                serializer = self.get_serializer(homework)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            message = {'error': f'The following arguments are expected: {expected_field}.'}
        errors = serializer.errors
        return Response(message or errors, status=status.HTTP_400_BAD_REQUEST)

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def update(self, request, *args, **kwargs):
        """Update selected homework for selected lection."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def destroy(self, request, *args, **kwargs):
        """Delete selected homework for selected lection."""
        homework = self.get_object()
        homework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def all(self, request, *args, **kwargs):
        """
        List all homeworks from all courses for authorized user depending on his role.
        """
        user = self.request.user
        role_user_id = getattr(user, user.role).id
        homework_role_dict = {
            'teacher': Homework.objects.filter(lection__course__teachers__id=role_user_id),
            'student': Homework.objects.filter(lection__course__students__id=role_user_id),
        }
        queryset = homework_role_dict[user.role]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
