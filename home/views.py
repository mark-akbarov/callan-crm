from django.shortcuts import render, redirect
from core.utils.alfa_crm import create_lead
from .forms import UserForm


def index(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            # course_name = form.cleaned_data['course_name']
            create_lead(
                name=f"{first_name} {last_name}",
                phone=phone_number,
                note=f"test"
            )
            return redirect("home:index")
    else:
        form = UserForm()
    return render(request, "home/index.html", context={"title": "test title", "form": form})
