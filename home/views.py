from django.shortcuts import render
# from .forms import UserForm


def index(request):
    # if request.method == 'POST':
    #     form = UserForm(data=request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         user[""]
    return render(request, "home/base.html", context={"title": "test title"})
    # return render(request, "home/index.html", context={"title": "test title"})
