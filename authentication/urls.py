from django.urls import path
from . import views
urlpatterns = [
    path('register', views.RegistrationView, name='register'),
    path('login', views.LoginView, name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate')
]