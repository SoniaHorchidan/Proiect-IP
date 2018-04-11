from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.login_view, name="login"),
    path('logout',views.logout_view, name="logout"),
    path('signup',views.signup, name="signup"),
	path('search', views.search_view, name="search"),
	path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile'),
]
