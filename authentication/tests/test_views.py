from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from utils.setup_test import TestSetup
class TestViews(TestCase):

    def test_should_show_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"auth/register.html")

    def test_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"auth/login.html")

    #test signup page
    # if succcessss
    def test_should_signup_user(self):
        self.user={
            "username": "username",
            "email":"email@gmail.com",
            "password":"password",
            "password2":"password",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        success = []
        for message in storage:
            success.append(message.message)
        self.assertIn("Account created successfully", list(map(lambda x: x.message, storage)))

    #check not null
    def test_should_signup_user_1(self):
        self.user={
            "username": "",
            "email":"email@gmail2.com",
            "password":"password",
            "password2":"password",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 409)
        storage = get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Please input your username", list(map(lambda x: x.message, storage)))

    def test_should_signup_user_2(self):
        self.user={
            "username": "username",
            "email":"",
            "password":"password",
            "password2":"password",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 409)
        storage = get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Please input your email", list(map(lambda x: x.message, storage)))

    def test_should_signup_user_3(self):
        self.user={
            "username": "username",
            "email":"email@gmail2.com",
            "password":"",
            "password2":"password",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 409)
        storage = get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Please input the password", list(map(lambda x: x.message, storage)))

    def test_should_signup_user_4(self):
        self.user={
            "username": "username",
            "email":"email@gmail2.com",
            "password":"password",
            "password2":"",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 409)
        storage = get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Please reconfirm the password", list(map(lambda x: x.message, storage)))

    #invalid email
    def test_should_signup_user_5(self):
        self.user={
            "username": "username",
            "email":"emailgmail2.com",
            "password":"password",
            "password2":"password",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 409)
        storage= get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Please provide a valid email", list(map(lambda x: x.message, storage)))

    #check password
    def test_should_signup_user_6(self):
        self.user={
            "username": "username",
            "email":"email@gmail2.com",
            "password":"pass",
            "password2":"pass",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 409)
        storage= get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Password should be at least 6 characters", list(map(lambda x: x.message, storage)))

    def test_should_signup_user_7(self):
        self.user={
            "username": "username",
            "email":"email@gmail2.com",
            "password":"password",
            "password2":"password2",
        }
        response = self.client.post(reverse("register"),self.user)
        self.assertEquals(response.status_code, 409)
        storage= get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Passwords do not match", list(map(lambda x: x.message, storage)))


    #same username
    def test_should_signup_user_8(self):
        self.user={
            "username": "username",
            "email":"email@gmail2.com",
            "password":"password",
            "password2":"password",
        }
        self.user2={
            "username": "username",
            "email":"email@gmail21.com",
            "password":"password",
            "password2":"password",
        }
        self.client.post(reverse("register"), self.user)
        response = self.client.post(reverse("register"),self.user2)
        self.assertEquals(response.status_code, 409)
        storage = get_messages(response.wsgi_request)
        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Username has already exist", list(map(lambda x: x.message, storage)))

    #same email
    def test_should_signup_user_9(self):
        self.user={
            "username": "username",
            "email":"email@gmail2.com",
            "password":"password",
            "password2":"password",
        }
        self.user2={
            "username": "username1",
            "email":"email@gmail2.com",
            "password":"password",
            "password2":"password",
        }
        self.client.post(reverse("register"), self.user)
        response = self.client.post(reverse("register"),self.user2)
        self.assertEquals(response.status_code, 409)
        storage= get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Email has already exist", list(map(lambda x: x.message, storage)))


    #test signin page
    # if succcessss
    def test_should_signin_user(self):
        self.user={
            "username": "username",
            "email":"email@gmail.com",
            "password":"password",
            "password2":"password",
        }
        self.client.post(reverse("register"),self.user)

        self.user2={
            "username": "username",
            "password":"password",
        }
        response = self.client.post(reverse("login"), self.user2)

        self.assertEquals(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        success = []
        for message in storage:
            success.append(message.message)
        self.assertIn("Account created successfully", list(map(lambda x: x.message, storage)))

    # if not null
    def test_should_signin_user_1(self):
        self.user={
            "username": "",
            "password":"password",
        }
        response = self.client.post(reverse("login"),self.user)
        self.assertEquals(response.status_code, 401)
        storage = get_messages(response.wsgi_request)
        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Please input your username", list(map(lambda x: x.message, storage)))

    def test_should_login_user_2(self):
        self.user={
            "username": "username",
            "password":"",
        }
        response = self.client.post(reverse("login"),self.user)
        self.assertEquals(response.status_code, 401)
        storage = get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Please input your password", list(map(lambda x: x.message, storage)))
    
    #check authen
    def test_should_login_user_3(self):
        self.user={
            "username": "username",
            "email":"email@gmail.com",
            "password":"password",
            "password2":"password",
        }
        self.client.post(reverse("register"),self.user)

        self.user2={
            "username": "username",
            "password":"password2",
        }
        response = self.client.post(reverse("login"), self.user2)
        self.assertEquals(response.status_code, 401)
        storage = get_messages(response.wsgi_request)

        errors = []
        for message in storage:
            errors.append(message.message)
        self.assertIn("Wrong username or password", list(map(lambda x: x.message, storage)))




    