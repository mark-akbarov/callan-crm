from django.views.generic import ListView
from course.models.course import Course


class CourseListView(ListView):
    model = Course
    context_object_name = 'course_list'
    template_name = 'course/course_list.html'