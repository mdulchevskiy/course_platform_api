# Generated by Django 3.1.4 on 2020-12-09 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='mark',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='course_api.mark'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='students',
            field=models.ManyToManyField(null=True, related_name='homeworks', through='course_api.Mark', to='course_api.Student'),
        ),
        migrations.AlterField(
            model_name='lection',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lections', to='course_api.course'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='homework',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='course_api.homework'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='course_api.student'),
        ),
    ]
