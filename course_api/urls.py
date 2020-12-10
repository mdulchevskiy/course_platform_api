from django.urls import (include,
                         path, )
from course_api.views import (LoginView,
                              RegistrationView, )
from course_api.routers import (course_router,
                                homework_router,
                                lection_router,
                                mark_router,
                                student_router,
                                teacher_router, )


urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('', include(course_router.urls)),
    path('courses/<int:course_id>/', include(student_router.urls)),
    path('courses/<int:course_id>/', include(teacher_router.urls)),
    path('courses/<int:course_id>/', include(lection_router.urls)),
    path('courses/<int:course_id>/lections/<int:lection_id>/', include(homework_router.urls)),
    path('courses/<int:course_id>/lections/<int:lection_id>/', include(mark_router.urls)),
]
