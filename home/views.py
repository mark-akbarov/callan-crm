from django.shortcuts import render, HttpResponse
from .forms import UserForm


def index(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            phone_number = form.cleaned_data['phone_number']
            birth_date = form.cleaned_data['birth_date']
            course_name = form.cleaned_data['course_name']
            print(first_name, phone_number, birth_date, course_name)
            return HttpResponse("Success!")
    else:
        form = UserForm()
    return render(request, "home/base.html", context={"title": "test title", "form": form})
    # return render(request, "home/index.html", context={"title": "test title"})
