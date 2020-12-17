from django.utils.decorators import method_decorator
from rest_framework import (permissions,
                            status,
                            viewsets, )
from rest_framework.decorators import action
from rest_framework.response import Response
from course_api.models import (Course,
                               Student, )
from course_api.serializers import StudentSerializer
from course_api.tools import access_to_course_validation_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.filter(id=course_id).first()
        return course_id, course

    def get_queryset(self):
        """Return students on selected course."""
        course_id, _ = self.get_course()
        return Student.objects.filter(courses__id=course_id)

    @access_to_course_validation_decorator
    def list(self, request, *args, **kwargs):
        """List all students on selected course."""
        return super().list(self, request, *args, **kwargs)

    @access_to_course_validation_decorator
    def retrieve(self, request, *args, **kwargs):
        """Detail selected student on selected course."""
        return super().retrieve(self, request, *args, **kwargs)

    @access_to_course_validation_decorator
    def create(self, request, *args, **kwargs):
        """
        Add student to selected course. POST method must include student id field "id".
        If expected field wasn't found or student doesn't exist, raise the error.
        """
        course_id, course = self.get_course()
        serializer = self.get_serializer(data=request.data)
        student_id = serializer.initial_data.get('id')
        student = Student.objects.filter(id=student_id).first()
        if student:
            course.students.add(student)
            return Response(status=status.HTTP_201_CREATED)
        else:
            message = f"Student with ID{student_id} doesn't exist."
        if not student_id:
            message = 'The following arguments are expected: id.'
        return Response({'error': f'{message}'}, status=status.HTTP_400_BAD_REQUEST)

    @access_to_course_validation_decorator
    def destroy(self, request, *args, **kwargs):
        """Remove selected student from selected course."""
        course_id, course = self.get_course()
        student = self.get_object()
        course.students.remove(student)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def all(self, request, *args, **kwargs):
        """
        List all registered students if authorized user is teacher.
        If authorized user is student, list all his coursemates from all his courses.
        """
        user = self.request.user
        user_role_id = getattr(user, user.role).id
        student_role_dict = {
            'student': Student.objects.filter(courses__students__id=user_role_id).distinct(),
            'teacher': Student.objects.all(),
        }
        queryset = student_role_dict[user.role]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
