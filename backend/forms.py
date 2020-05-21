from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Poprawny adres e-mail', widget=forms.TextInput
    (attrs={'placeholder': 'E-mail'}))
    name = forms.CharField(max_length=254, help_text="Imię i nazwisko", widget=forms.TextInput
    (attrs={'placeholder': 'Imię i nazwisko'}))
    phone = forms.CharField(max_length=128, help_text="Telefon kontaktowy", required=False, widget=forms.TextInput
    (attrs={'placeholder': 'telefon kontaktowy'}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'name', 'phone')
