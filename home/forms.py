from django import forms

from account.models import User


class UserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ism'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Familiya'}))
    birth_date = forms.DateField(widget=forms.TextInput())
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+998'}))
    course_name = forms.CharField(widget=forms.TextInput())
