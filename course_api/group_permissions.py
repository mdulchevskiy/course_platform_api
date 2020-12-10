from django.contrib.auth.models import Permission


def get_group_permissions():
    """Return dict with permissions for user groups."""
    group_permissions = {
        'student': [
            Permission.objects.get(codename='view_course'),

            Permission.objects.get(codename='view_homework'),

            Permission.objects.get(codename='view_teacher'),

            Permission.objects.get(codename='view_student'),

            Permission.objects.get(codename='change_mark'),
            Permission.objects.get(codename='view_mark'),

            Permission.objects.get(codename='view_lection'),
        ],
        'teacher': [
            Permission.objects.get(codename='add_course'),
            Permission.objects.get(codename='change_course'),
            Permission.objects.get(codename='delete_course'),
            Permission.objects.get(codename='view_course'),

            Permission.objects.get(codename='add_homework'),
            Permission.objects.get(codename='change_homework'),
            Permission.objects.get(codename='delete_homework'),
            Permission.objects.get(codename='view_homework'),

            Permission.objects.get(codename='add_teacher'),
            Permission.objects.get(codename='delete_teacher'),
            Permission.objects.get(codename='view_teacher'),

            Permission.objects.get(codename='add_student'),
            Permission.objects.get(codename='delete_student'),
            Permission.objects.get(codename='view_student'),

            Permission.objects.get(codename='change_mark'),
            Permission.objects.get(codename='view_mark'),

            Permission.objects.get(codename='add_lection'),
            Permission.objects.get(codename='change_lection'),
            Permission.objects.get(codename='delete_lection'),
            Permission.objects.get(codename='view_lection'),
        ],
    }
    return group_permissions
