from django import forms

from account.models import User
from course.models import Course

input_style = 'width: 90%; margin: 0 auto; padding: 8px; border: 1px solid #ccc; border-radius: 4px'
class UserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ism', 'style': input_style}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Familiya', 'style': input_style}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+998', 'style': input_style}))
    courses = forms.ModelChoiceField(
        label="Kurslar",
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'custom-class', 'style': input_style}),
    )
