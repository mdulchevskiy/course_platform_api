from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = ['student', 'teacher']
ROLE_CHOICES = [(role, role) for role in ROLES]
HOMEWORK_STATUSES = ['set', 'done']
STATUS_CHOICES = [(status, status) for status in HOMEWORK_STATUSES]


class PlatformUser(AbstractUser):
    username = models.CharField(max_length=30, default=None, unique=True)
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=50, default=None)
    password = models.CharField(max_length=30, default=None)
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default='student')

    def __str__(self):
        return f'user {self.pk}: {self.username}'


class Course(models.Model):
    name = models.CharField(max_length=128, default=None, unique=True)

    def __str__(self):
        return f'course {self.pk}: {self.name}'


class Teacher(models.Model):
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=50, default=None)
    user = models.OneToOneField('PlatformUser', related_name='teacher', on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', related_name='teachers')

    def __str__(self):
        return f'teacher {self.pk}: {self.first_name} {self.last_name}'


class Student(models.Model):
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=50, default=None)
    user = models.OneToOneField('PlatformUser', related_name='student', on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', related_name='students')

    def __str__(self):
        return f'student {self.pk}: {self.first_name} {self.last_name}'


class Lection(models.Model):
    topic = models.CharField(max_length=255, default=None, null=True, unique=True)
    presentation = models.FileField(default=None, null=True, upload_to='presentations/')
    course = models.ForeignKey('Course', null=True, related_name='lections', on_delete=models.CASCADE)

    def __str__(self):
        return f'lection {self.pk}: {self.topic}'


class Homework(models.Model):
    task = models.CharField(max_length=255, default=None, unique=True)
    lection = models.ForeignKey('Lection', null=True, related_name='homeworks', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student', related_name='homeworks', through='Mark')

    def __str__(self):
        return f'homework: {self.pk}'


class Mark(models.Model):
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='set')
    solution = models.CharField(max_length=1100, default=None, null=True)
    mark = models.IntegerField(default=None, null=True)
    student = models.ForeignKey('Student', null=True, related_name='marks', on_delete=models.CASCADE)
    homework = models.ForeignKey('Homework', null=True, related_name='marks', on_delete=models.CASCADE)

    def __str__(self):
        return f'mark: {self.pk}'


class Comment(models.Model):
    comment = models.CharField(max_length=255, default=None)
    mark = models.ForeignKey('Mark', null=True, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'comment: {self.pk}'
