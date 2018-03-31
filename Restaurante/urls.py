from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name="login"),
    path('logout',views.logout_view, name="logout"),
    path('signup',views.UserCreateView.as_view(), name="signup"),
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile'),
]
