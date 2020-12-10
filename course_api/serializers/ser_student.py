from rest_framework import serializers
from course_api.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name')

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Not a valid name: only letters are allowed.')
        return value.capitalize()

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Not a valid surname: only letters are allowed.')
        return value.capitalize()
