from django.shortcuts import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from Restaurante.forms import LoginForm, SignUpForm
from Restaurante.models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, View


def index(request):
    return render( request, 'index.html')

def home(request):
    return render( request, 'home.html')

def login_view(request):
    context = {}
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request=request,
                      user=user)
                return redirect('home')
            else:
                context['error_message'] = 'Wrong username or password!'
    context['form'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')

class UserProfileDetailView(DetailView):
    template_name = 'profile.html'
    model = UserProfile
    context_object_name = 'userprofile'


class UserCreateView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    model = UserProfile

    def get_success_url(self, *args, **kwargs):
        return reverse('login')

    def signup(request):
        if request.method == 'POST':
            form = UserCreateForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user=authenticate(username=username,password=password)
                return redirect('login')
        else:
            form = UserCreateForm()
        return render(request, 'signup.html', {'form': form})
