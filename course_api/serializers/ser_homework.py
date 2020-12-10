from rest_framework import serializers
from course_api.models import Homework
from course_api.serializers.ser_lection import LectionSerializer


class HomeworkSerializer(serializers.ModelSerializer):
    lection = LectionSerializer(read_only=True)

    class Meta:
        model = Homework
        fields = ('id', 'task', 'lection')
