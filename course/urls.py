from django.urls import path
from course.views.course import CourseListView


urlpatterns = [
    path('courses/', CourseListView.as_view())
]
