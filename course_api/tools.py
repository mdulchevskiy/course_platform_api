import functools
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from course_api.models import (Course,
                               Lection, )


def access_to_course_validation_decorator(method):
    @functools.wraps(method)
    def access_validation(self, request, *args, **kwargs):
        """
        Wraps a ModelViewSet method for course validation. Course validation
        includes checking existence of selected course and checking that the
        authorized user belongs to selected course.
        """
        course_id = self.kwargs.get('course_id')
        user = self.request.user
        user_role_id = getattr(user, user.role).id
        course_role_dict = {
            'teacher': Course.objects.filter(Q(teachers__id=user_role_id) & Q(id=course_id)),
            'student': Course.objects.filter(Q(students__id=user_role_id) & Q(id=course_id)),
        }
        course = course_role_dict[user.role]
        error = {'error': f"Either you don't have access to this course, "
                          f"or course with ID{course_id} doesn't exist."}
        if course:
            return method(self, request, *args, **kwargs)
        return Response(error, status=status.HTTP_403_FORBIDDEN)
    return access_validation


def lection_existence_validation_decorator(method):
    @functools.wraps(method)
    def existence_validation(self, request, *args, **kwargs):
        """
        Wraps a ModelViewSet method for lection validation. Lection validation
        includes checking existence of selected lection and checking that the
        selected lection belongs to selected course.
        """
        lection_id = self.kwargs.get('lection_id')
        course_id = self.kwargs.get('course_id')
        lection = Lection.objects.filter(Q(course_id=course_id) & Q(id=lection_id)).first()
        error = {'error': f"Either lection with ID{lection_id} doesn't belong to course with ID{course_id}, "
                          f"or doesn't exist."}
        if lection:
            return method(self, request, *args, **kwargs)
        return Response(error, status=status.HTTP_403_FORBIDDEN)
    return existence_validation


def openapi_ready(model):
    """
    Decorator for avoiding swagger openapi exception during schema generation:
    "AttributeError: 'AnonymousUser' object has no attribute 'role'."
    """
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if getattr(self, "swagger_fake_view", False):
                return model.objects.none()
            else:
                return method(self, *args, **kwargs)
        return wrapper
    return decorator
