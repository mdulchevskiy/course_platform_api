from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import (permissions,
                            status,
                            viewsets, )
from rest_framework.decorators import action
from rest_framework.response import Response
from course_api.models import (Comment,
                               Course,
                               Lection,
                               Mark, )
from course_api.serializers import (CommentSerializer,
                                    MarkSerializer, )
from course_api.tools import (access_to_course_validation_decorator,
                              lection_existence_validation_decorator,
                              openapi_ready, )
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="""
        Update selected homework mark for selected lection.
        Can update field "solution" if authorized user is student. If authorized user is teacher,
        can update field "mark". Also add comments for selected homework mark.
    """))
class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    @staticmethod
    def clear_mark_data(mark_data, option=None):
        if option == 'student':
            for mark in mark_data:
                mark.pop('student')
                mark['homework'].pop('lection')
        elif option == 'teacher':
            for mark in mark_data:
                mark['homework'].pop('lection')
        return mark_data

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.filter(id=course_id).first()
        return course_id, course

    def get_lection(self):
        course_id, _ = self.get_course()
        lection_id = self.kwargs.get('lection_id')
        lection = Lection.objects.filter(Q(course_id=course_id) & Q(id=lection_id)).first()
        return lection_id, lection

    @openapi_ready(Mark)
    def get_queryset(self):
        """
        Return homework marks for selected lection for authorized student. If authorized user
        is teacher, return homework marks with status "done" for all students for selected lection.
        """
        user = self.request.user
        user_role_id = getattr(user, user.role).id
        lection_id, _ = self.get_lection()
        mark_role_dict = {
            'student': Mark.objects.filter(Q(homework__lection__id=lection_id) & Q(student_id=user_role_id)),
            'teacher': Mark.objects.filter(Q(homework__lection__id=lection_id) & Q(status='done')),
        }
        return mark_role_dict[user.role]

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def list(self, request, *args, **kwargs):
        """List all homeworks (mark object) for selected lection."""
        user = self.request.user
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(self.clear_mark_data(serializer.data, option=user.role))

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def retrieve(self, request, *args, **kwargs):
        """Detail selected homework (mark object) for selected lection."""
        return super().retrieve(self, request, *args, **kwargs)

    @lection_existence_validation_decorator
    @access_to_course_validation_decorator
    def update(self, request, *args, **kwargs):
        """
        Update selected homework mark for selected lection.
        Can update field "solution" if authorized user is student. If authorized user is teacher,
        can update field "mark". Also add comments for selected homework mark.
        """
        user = self.request.user

        mark = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if user.role == 'student':
                solution = serializer.validated_data.get('solution')
                if solution:
                    setattr(mark, 'solution', solution)
                    setattr(mark, 'status', 'done')
                    mark.save()
            else:
                rate = serializer.validated_data.get('mark')
                if rate:
                    setattr(mark, 'mark', rate)
                    mark.save()
        errors = serializer.errors

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.validated_data.get('comment')
            if comment:
                serializer.save()
                comment_object = Comment.objects.filter(id=serializer.data['id'])
                with transaction.atomic():
                    comment_object.update(comment=f'{user.first_name} {user.last_name}: {comment}')
                    mark.comments.add(comment_object.first())
        errors.update(serializer.errors)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(mark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def all(self, request, *args, **kwargs):
        """
        List all homeworks (mark object) for all courses if authorized user is student.
        If authorized user is teacher, list all done homeworks (mark object) for selected lection.
        """
        user = self.request.user
        role_user_id = getattr(user, user.role).id
        mark_role_dict = {
            'teacher': Mark.objects.filter(Q(homework__lection__course__teachers__id=role_user_id) &
                                           Q(status='done')),
            'student': Mark.objects.filter(student_id=role_user_id),
        }
        queryset = mark_role_dict[user.role]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def rated(self, request, *args, **kwargs):
        """
        List all rated homeworks (mark object) for all courses if authorized user is student.
        If authorized user is teacher, list all rated homeworks (mark object) for selected lection.
        """
        user = self.request.user
        role_user_id = getattr(user, user.role).id
        mark_role_dict = {
            'teacher': Mark.objects.filter(Q(homework__lection__course__teachers__id=role_user_id) &
                                           Q(mark__isnull=False)),
            'student': Mark.objects.filter(Q(student_id=role_user_id) & Q(mark__isnull=False)),
        }
        queryset = mark_role_dict[user.role]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
