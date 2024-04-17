from django import forms

from account.models import User
from course.models import Course


class UserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ism'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Familiya'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+998'}))
    courses = forms.ModelChoiceField(
        label="Kurslar",
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'custom-class'})
    )
