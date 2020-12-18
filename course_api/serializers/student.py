from rest_framework import serializers
from course_api.models import Student
from course_api.validators import isalpha_validator


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'validators': [isalpha_validator]},
            'last_name': {'validators': [isalpha_validator]},
        }
