from django.urls import path
from courses.views import CoursesHomeView, CourseDetailView, SectorCoursesView, SearchCourseView, AddComment

urlpatterns = [
    path('',CoursesHomeView.as_view()),
    path('detail/<uuid:course_uuid>/',CourseDetailView.as_view()),
    path('sector/<uuid:sector_uuid>/',SectorCoursesView.as_view()),
    path("search/<str:search_term>/",SearchCourseView.as_view()),
    path('comment/<uuid:course_uuid>/',AddComment.as_view()),
]