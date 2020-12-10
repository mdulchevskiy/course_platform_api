from rest_framework.routers import DefaultRouter
from course_api.views import (CourseViewSet,
                              HomeworkViewSet,
                              LectionViewSet,
                              MarkViewSet,
                              StudentViewSet,
                              TeacherViewSet, )


course_router = DefaultRouter()
homework_router = DefaultRouter()
lection_router = DefaultRouter()
mark_router = DefaultRouter()
student_router = DefaultRouter()
teacher_router = DefaultRouter()

course_router.register('courses', CourseViewSet, basename='course-list')
homework_router.register('homeworks', HomeworkViewSet, basename='homework-list')
lection_router.register('lections', LectionViewSet, basename='lection-list')
mark_router.register('marks', MarkViewSet, basename='mark-list')
student_router.register('students', StudentViewSet, basename='student-list')
teacher_router.register('teachers', TeacherViewSet, basename='teacher-list')
