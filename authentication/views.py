from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from authentication.decorators import auth_user_should_not_access
import threading
class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('auth/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()

@auth_user_should_not_access
def RegistrationView(request):
    if request.method == "POST":
        context={
            'data' : request.POST,
        }

        email=request.POST.get('email')
        username =request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        #check not null      
        if username == '':
            messages.add_message(request, messages.ERROR, 'Please input your username')
            return render(request, 'auth/register.html', context=context, status=409)

        if email == '':
            messages.add_message(request, messages.ERROR, 'Please input your email')
            return render(request, 'auth/register.html', context=context, status=409)

        if password == '':
            messages.add_message(request, messages.ERROR, 'Please input the password')
            return render(request, 'auth/register.html', context=context, status=409)
        
        if password2 == '':
            messages.add_message(request, messages.ERROR, 'Please reconfirm the password')
            return render(request, 'auth/register.html', context=context, status=409)
        
        #check valid email and password
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Please provide a valid email')
            return render(request, 'auth/register.html', context=context, status=409)
        
        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password should be at least 6 characters')
            return render(request, 'auth/register.html', context=context, status=409)

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            return render(request, 'auth/register.html', context=context, status=409)
            
        
        #check exist email or username
        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email has already exist')
                return render(request, 'auth/register.html', context=context, status=409)
         
        except Exception as identifier:
            pass
    
        try:
            if User.objects.get(username = username):
                messages.add_message(request, messages.ERROR, 'Username has already exist')
                return render(request, 'auth/register.html', context=context, status=409)
        
        except Exception as identifier:
            pass
    
        
        user=User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_email_verified = False    
        user.save()

        send_activation_email(user, request)

        messages.add_message(request, messages.SUCCESS, 'Account created successfully')
        
        return redirect('login')
    return render(request, 'auth/register.html')

@auth_user_should_not_access
def LoginView(request):
    if request.method == "POST":
        context={
            'data':request.POST,
        }

        username=request.POST.get('username')
        password=request.POST.get('password')

        #check not null
        if username =='':
            messages.add_message(request, messages.ERROR, 'Please input your username')
            return render(request,'auth/login.html',status=401, context=context)

        if password =='':
            messages.add_message(request, messages.ERROR, 'Please input your password')
            return render(request,'auth/login.html',status=401, context=context)

        user=authenticate(request,username=username, password=password)
        
        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR, 'Email is not verified')
            login(request, user)
            return redirect('home')
        
        
        if not user:
            messages.add_message(request, messages.ERROR, 'Wrong username or password')
            return render(request,'auth/login.html',status=401, context=context)
        
        login(request, user)

        return redirect('home')
    return render(request, 'auth/login.html')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None

        if user is not None and generate_token.check_token(user, token):
            user.is_email_verified=True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Account activated successfully')
            return redirect('login')
        
        return render(request, 'auth/activate_failed.html', status=401)

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')