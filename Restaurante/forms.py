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
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'birth_date', 'preferences', )
        help_texts = {
            'preferences': 'Select one or more food preferences',
            'last_name': 'Required.',
            'first_name': 'Required'
        }

    def custom_save(self, datas):
        user = User.objects.create_user(datas['username'],
                                     first_name=datas['first_name'],
                                     last_name=datas['last_name'],
                                     email=datas['email'],
                                     password=datas['password1'],
                                     )
        user.is_active = False
        user.profile.birth_date = datas['birth_date']
        user.profile.preferences.set(datas['preferences'])
        user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'preferences')
