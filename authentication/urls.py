from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('register', views.RegistrationView, name='register'),
    path('login', views.LoginView, name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate')
]