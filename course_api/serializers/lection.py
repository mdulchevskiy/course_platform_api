from rest_framework import serializers
from course_api.models import Lection


class LectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lection
        fields = ('id', 'topic', 'presentation', 'course')
        depth = 1
