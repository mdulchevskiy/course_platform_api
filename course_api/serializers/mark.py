from rest_framework import serializers
from course_api.models import Mark
from course_api.serializers.comment import CommentSerializer
from course_api.serializers.homework import HomeworkSerializer
from course_api.serializers.student import StudentSerializer


class MarkSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    homework = HomeworkSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Mark
        fields = ('id', 'status', 'solution', 'mark', 'comments', 'student', 'homework')
        depth = 1
