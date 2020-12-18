from rest_framework import serializers
from course_api.models import Teacher
from course_api.validators import isalpha_validator


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'validators': [isalpha_validator]},
            'last_name': {'validators': [isalpha_validator]},
        }
