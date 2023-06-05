from django.urls import path
from courses.views import CoursesHomeView

urlpatterns = [
    path('',CoursesHomeView.as_view()),
]