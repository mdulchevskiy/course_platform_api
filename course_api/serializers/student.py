from rest_framework import serializers
from course_api.models import Student
from course_api.validators import isalpha_validator


class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, validators=[isalpha_validator])
    last_name = serializers.CharField(max_length=50, validators=[isalpha_validator])

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name')
