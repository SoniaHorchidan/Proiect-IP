from django import forms
from django.contrib.auth.forms import UserCreationForm
from Restaurante.models import Profile, Keyword, Restaurant
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    preferences = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'birth_date', 'preferences', )
