from rest_framework import serializers
from course_api.models import Course
from course_api.serializers.lection import LectionSerializer
from course_api.serializers.student import StudentSerializer
from course_api.serializers.teacher import TeacherSerializer


class CourseSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    lections = LectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'teachers', 'students', 'lections')
        depth = 1
