from rest_framework import serializers
from course_api.models import Course
from course_api.serializers.ser_lection import LectionSerializer
from course_api.serializers.ser_student import StudentSerializer
from course_api.serializers.ser_teacher import TeacherSerializer


class CourseSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    lections = LectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'teachers', 'students', 'lections')
        depth = 1
