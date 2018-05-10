from django.shortcuts import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from Restaurante.forms import LoginForm, SignUpForm, UserForm, ProfileForm
from Restaurante.models import Profile, Restaurant
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, View
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from Restaurante.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.http import Http404
from Restaurante.manageRequest import RequestsManager
import json
from django.contrib import messages
from Restaurante.models import Keyword
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def favorites_around_request(request):
    if request.is_ajax:
        if len(request.GET) == 0:
            raise Http404

        res = request.GET.getlist('names[]')
        current_user = request.user.id

        profile = User.objects.filter(id__in=[current_user])[0]
        profile = Profile.objects.filter(user__in=[profile])[0]

        result = profile.favourites.all()
        result = [el.name for el in result]
        result = [el for el in result if el in res]
        
        print(result)

        return HttpResponse(json.dumps(result))


def search_request(request):
    if request.is_ajax:
        if len(request.GET) == 0:
            raise Http404

        res = request.GET.getlist('names[]')
        current_user = request.user.id
        manager = RequestsManager(current_user)
        #result = manager.manage(['Restaurant1', 'Restaurant3', 'Restaurant2'], 25)
        result = manager.manage(res)

        return HttpResponse(json.dumps(result))

def index(request):
    if is_authenticated(request.user) == True:
        return render( request, 'home.html')
    else:
        return render( request, 'index.html')

@login_required
def home(request):
    return render( request, 'home.html')

def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    return user.is_authenticated

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
                if user.profile.email_confirmed is True:
                    login(request=request,
                          user=user)
                    return redirect('home')
                else:
                    context['error_message'] = 'Your account has not been confirmed yet!'
            else:
                context['error_message'] = 'Wrong username or password! Please try again!'
    context['form'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')

@login_required
def search_view(request):
	context = {}
	return render(request, 'search.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.first_name = form.cleaned_data.get('first_name')
            if form.cleaned_data.get('preferences').count() > 5:
                return render(request, 'signup.html', {'form': form, 'error_message': 'You cannot have more than 5 preferences at a time!:('})
            user.profile.preferences.set(form.cleaned_data.get('preferences'))
            user.save()
            raw_password = form.cleaned_data.get('password1')
            current_site = get_current_site(request)
            subject = 'Activate Your !Starve Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                'token': str(account_activation_token.make_token(user)),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')           
    else:
        form = SignUpForm()
    keywords = Keyword.objects.all();
    return render(request, 'signup.html', {'form': form, 'keywords': keywords})


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    model = Profile
    context_object_name = 'userprofile'

class SearchPageListView(LoginRequiredMixin, ListView):
    template_name = 'find.html'
    model = Restaurant
    context_object_name = 'items'
    def get_queryset(self):
        searchInput = self.kwargs['input']
        queryset = Restaurant.objects.filter(name__contains=searchInput).all()
        return queryset

class SearchPageListView1(LoginRequiredMixin, ListView):
    template_name = 'find1.html'
    model = Restaurant
    context_object_name = 'items'
    def get_queryset(self):
        queryset = Restaurant.objects.all()
        return queryset

class AddedFavoriteView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
        obj = Restaurant.objects.get(pk=kwargs['pk'])
        if obj not in request.user.profile.favourites.all():
            request.user.profile.favourites.add(obj)
            request.user.profile.save()
            return render( request, 'favorite.html', {'response': 'The restaurant was added to your favorites list!'})
        else:
            request.user.profile.favourites.remove(obj)
            request.user.profile.save()
            return render( request, 'favorite.html', {'response': 'The restaurant was removed from your favorites list!'})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

@login_required
def update_profile(request, pk):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = Profile.objects.get(pk=pk)
            profile.trained = False
            if profile_form.cleaned_data.get('preferences').count() > 5:
                return render(request, 'edit_profile.html', {'form': profile_form, 'error_message': 'You cannot have more than 5 preferences at a time!:('})
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            #return render(request, 'profile.html', {'pk': pk})
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def redirect_to_index(request):
    return redirect('index')

def loaderIO(request):
	context={}
	return render(request, 'loaderIOFile.html', context)