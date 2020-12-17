from rest_framework import serializers
from course_api.models import Teacher
from course_api.validators import isalpha_validator


class TeacherSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, validators=[isalpha_validator])
    last_name = serializers.CharField(max_length=50, validators=[isalpha_validator])

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name')
