from django.contrib.auth.models import Group
from rest_framework import serializers
from course_api.group_permissions import get_group_permissions
from course_api.models import (PlatformUser,
                               Student,
                               Teacher, )
from course_api.validators import isalpha_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'role')
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'required': True},
            'first_name': {'validators': [isalpha_validator]},
            'last_name': {'validators': [isalpha_validator]},
        }

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError('Not a valid username: only letters and numbers are allowed.')
        return value

    def validate_password(self, value):
        if any(lit.isspace() for lit in value):
            raise serializers.ValidationError("Not a valid password: whitespaces aren't allowed.")
        return value

    def create(self, validated_data):
        """
        Check user groups existence and create them with assigment of permissions if don't exist.
        Create user. Create teacher or student according to user's role.
        Add user to group according to his role.
        """
        role = validated_data.get('role')
        group, created = Group.objects.get_or_create(name=role)
        if created:
            group_permissions = get_group_permissions()
            group.permissions.set(group_permissions[group.name])

        user = PlatformUser.objects.create(**validated_data)
        group.user_set.add(user)

        models_dict = {
            'teacher': Teacher.objects.create,
            'student': Student.objects.create,
        }
        models_dict[role](
            first_name=user.first_name,
            last_name=user.last_name,
            user=user,
        )
        return user
