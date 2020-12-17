from django.utils.decorators import method_decorator
from rest_framework import (permissions,
                            status,
                            viewsets, )
from rest_framework.decorators import action
from rest_framework.response import Response
from course_api.models import (Course,
                               Teacher, )
from course_api.serializers import TeacherSerializer
from course_api.tools import access_to_course_validation_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.filter(id=course_id).first()
        return course_id, course

    def get_queryset(self):
        """Return teachers from selected course."""
        course_id, _ = self.get_course()
        return Teacher.objects.filter(courses__id=course_id)

    @access_to_course_validation_decorator
    def list(self, request, *args, **kwargs):
        """List all teachers from selected course."""
        return super().list(self, request, *args, **kwargs)

    @access_to_course_validation_decorator
    def retrieve(self, request, *args, **kwargs):
        """Detail selected teacher from selected course."""
        return super().retrieve(self, request, *args, **kwargs)

    @access_to_course_validation_decorator
    def create(self, request, *args, **kwargs):
        """
        Add teacher to selected course. POST method must include teacher id field "id".
        If expected field wasn't found or teacher doesn't exist, raise the error.
        """
        course_id, course = self.get_course()
        serializer = self.get_serializer(data=request.data)
        teacher_id = serializer.initial_data.get('id')
        teacher = Teacher.objects.filter(id=teacher_id).first()
        if teacher:
            course.teachers.add(teacher)
            return Response(status=status.HTTP_201_CREATED)
        else:
            message = f"Teacher with ID{teacher_id} doesn't exist."
        if not teacher_id:
            message = 'The following arguments are expected: id.'
        return Response({'error': f'{message}'}, status=status.HTTP_400_BAD_REQUEST)

    @access_to_course_validation_decorator
    def destroy(self, request, *args, **kwargs):
        """Remove selected teacher from selected course."""
        course_id, course = self.get_course()
        teacher = self.get_object()
        course.teachers.remove(teacher)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def all(self, request, *args, **kwargs):
        """
        List all registered teachers if authorized user is teacher.
        If authorized user is student, list all his teachers from all his courses.
        """
        user = self.request.user
        role_user_id = getattr(user, user.role).id
        teacher_role_dict = {
            'student': Teacher.objects.filter(courses__students__id=role_user_id).distinct(),
            'teacher': Teacher.objects.all(),
        }
        queryset = teacher_role_dict[user.role]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
