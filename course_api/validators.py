from rest_framework import serializers


def isalpha_validator(value):
    if not value.isalpha():
        raise serializers.ValidationError('Not a valid field: only letters are allowed.')
    return value.capitalize()
