from django import forms
from django.contrib.auth.forms import UserCreationForm
from Restaurante.models import UserProfile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = []

    def save(self, commit=True):
        instance = super(SignUpForm, self).save(commit=False)
        user = User(username=self.data['username'],
                    password=self.data['password'],
                    email=self.data['email'],
                    first_name=self.data['first_name'],
                    last_name=self.data['last_name'])
        user.set_password(self.cleaned_data["password"])
        user.save()
        instance.user = user
        instance.save()
        return instance
