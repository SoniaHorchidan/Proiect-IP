from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.login_view, name="login"),
    path('logout',views.logout_view, name="logout"),
    path('signup',views.signup, name="signup"),
	path('search', views.search_view, name="search"),
	path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/update', views.update_profile, name = 'profile_update'),
	path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('search_request', views.search_request),
]
